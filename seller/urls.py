from django.urls import path

from .views import *

app_name = 'seller'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='seller-dashboard'),
    path('create-product/', ProductCreateView.as_view(), name='create-product'),
    path('edit-product/<int:id>/', ProductUpdateView.as_view(), name='edit-product'),
    path('update-shop/', ShopUpdateView.as_view(), name='update-shop')
]
