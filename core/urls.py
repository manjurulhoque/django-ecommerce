from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView
from graphene_django.views import GraphQLView

from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>/', remove_from_cart, name='remove-from-cart'),
    path('remove-quantity-from-cart/<int:id>/', remove_quantity_from_cart, name='remove-quantity-from-cart'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),

    # graphql
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
