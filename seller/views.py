from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import *


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    permission_denied_message = "You are not allowed to view this page"
    model = Product
    context_object_name = "products"
    template_name = "seller/dashboard.html"

    def test_func(self):
        return self.request.user.user_type == 'seller'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ProductCreateForm
    template_name = "seller/create-product.html"
    success_url = "/"
    permission_denied_message = "You are not allowed to view this page"

    def test_func(self):
        return self.request.user.user_type == 'seller'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Product successfully added')
        return super(ProductCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProductUpdateForm
    model = Product
    template_name = "seller/update-product.html"
    success_url = reverse_lazy("seller:seller-dashboard")
    permission_denied_message = "You are not allowed to view this page"
    slug_url_kwarg = 'id'
    slug_field = 'id'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def test_func(self):
        return self.request.user.user_type == 'seller'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Product successfully updated')
        return super(ProductUpdateView, self).form_valid(form)

    def get_object(self, queryset=None):
        obj = self.model.objects.get(id=self.kwargs['id'])
        if obj is None:
            raise Http404("Product doesn't exists")
        return obj
