import random
import string

import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View

from .forms import CheckoutForm
from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False)[0]
        if order.billing_address:
            context = {
                'order': order,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "u have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False)[0]
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order
            order.ordered = True
            order.payment = payment
            # TODO : assign ref code
            # order.ref_code = create_ref_code()
            order.save()

            messages.success(self.request, "Order was successful")
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "RateLimitError")
            print(e)
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            print(e)
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            print(e)
            messages.error(self.request, "Not Authentication")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.error(self.request, "Serious Error occured")
            return redirect("/")


class HomeView(ListView):
    template_name = "index.html"
    queryset = Product.objects.filter(is_active=True)
    context_object_name = 'items'


class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    context_object_name = "carts"
    template_name = "cart.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        carts = self.get_queryset()
        total = 0.0
        for cart in carts:
            total += cart.get_final_price()

        context['total'] = total
        return context

    def get_queryset(self):
        return Cart.objects.select_related('product').filter(user=self.request.user)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ShopView(ListView):
    model = Product
    paginate_by = 6
    template_name = "shop.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product-detail.html"
    slug_field = 'id'
    slug_url_kwarg = 'id'


class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        item = Product.objects.filter(category=category, is_active=True)
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "category.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            carts = Cart.objects.filter(user=self.request.user)[0]
            address = BillingAddress.objects.filter(user=self.request.user, save_info=True)[0]
            initial = {
                'street_address': address.street_address,
                'apartment_address': address.apartment_address,
                'country': address.country,
                'zip': address.zip,
            }
            form = CheckoutForm(initial=initial)
            context = {
                'form': form,
                'carts': carts,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active cart")
            return redirect("core:home")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            order = Order.objects.create(user=self.request.user)
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            # add functionality for these fields
            # same_shipping_address = form.cleaned_data.get(
            #     'same_shipping_address')
            # save_info = form.cleaned_data.get('save_info')
            payment_option = form.cleaned_data.get('payment_option')
            if payment_option not in ['S', 'P']:
                messages.warning(self.request, "Invalid payment option select")
                return redirect('core:checkout')

            billing_address = BillingAddress(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip,
                address_type='B',
                save_info=form.cleaned_data.get('save_info')
            )
            billing_address.save()
            carts = Cart.objects.filter(user=self.request.user)
            for cart in carts:
                order_item = OrderItem.objects.create(user=self.request.user, ordered=False, product=cart.product,
                                                      quantity=cart.quantity)
                order.items.add(order_item)

            carts.delete()

            order.shipping_address = billing_address
            order.billing_address = billing_address
            order.save()

            if payment_option == 'S':
                return redirect('core:payment', payment_option='stripe')
            elif payment_option == 'P':
                return redirect('core:payment', payment_option='paypal')
            else:
                messages.warning(self.request, "Invalid payment option select")
                return redirect('core:checkout')
        else:
            return render(self.request, 'checkout.html', {'form': form})


def add_to_cart(request, id):
    item = get_object_or_404(Product, id=id)
    if not item:
        return JsonResponse({'status': False, 'message': 'Product not found'}, safe=True)
    if not request.user.is_authenticated:
        return JsonResponse({'status': False, 'message': 'Please login to continue'}, safe=True)
    if Cart.objects.filter(user=request.user, product=item).exists():
        cart = Cart.objects.get(user=request.user, product=item)
        cart.quantity += 1
        cart.save()
    else:
        Cart.objects.create(user=request.user, product=item, quantity=1)

    # result = json.dumps(model_to_dict(item), cls=ExtendedEncoder)
    cart_total_items = Cart.objects.filter(user=request.user).count()

    return JsonResponse({'status': True, 'product_price': item.price, 'cart_total_items': cart_total_items,
                         'message': 'Successfully added to cart'},
                        safe=True)


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Cart, id=id)
    if item:
        item.delete()
        messages.info(request, "Product was removed from your cart.")
        return redirect("core:cart")
    else:
        messages.info(request, "Product was not in your cart.")
        return redirect("core:cart")


@login_required
def remove_quantity_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    # if quantity is 1 and we still need to decrease qty, then we will remove the item from cart
    if cart_item.quantity == 1:
        cart_item.delete()

        cart_total_items = Cart.objects.filter(user=request.user).count()
        return JsonResponse(
            {'status': True, 'product_price': cart_item.product.price, 'cart_total_items': cart_total_items,
             'message': 'Successfully removed quantity from the cart'},
            safe=True)
    cart_item.quantity -= 1
    cart_item.save()

    cart_total_items = Cart.objects.filter(user=request.user).count()

    return JsonResponse({'status': True, 'product_price': cart_item.product.price, 'cart_total_items': cart_total_items,
                         'message': 'Successfully removed quantity from the cart'},
                        safe=True)
