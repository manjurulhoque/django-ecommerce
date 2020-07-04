from django.urls import path

from core.api.views import *

urlpatterns = [
    # Product
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),

    # Category
    path('categories/', CategoryListAPIView.as_view(), name='api-category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='api-category-detail'),

    # Cart
    path('add-to-cart/<int:pk>/', add_to_cart_api, name='api-add-to-cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='api-remove-from-cart'),
    path('remove-quantity-from-cart/<int:pk>/', remove_quantity_from_cart, name='api-remove-quantity-from-cart'),
]
