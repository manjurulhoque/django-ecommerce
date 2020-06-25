from django.urls import path

from core.api.views import ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
]
