from django.urls import path

from core.api.views import *

urlpatterns = [
    # Product
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    # Category
    path('categories/', CategoryListAPIView.as_view(), name='api-category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='api-category-detail'),
]
