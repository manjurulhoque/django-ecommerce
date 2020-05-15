from django.urls import path

from .views import *

app_name = 'buyer'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='buyer-dashboard'),
    path('generate-invoice/<int:order_id>', generate_invoice, name='generate-invoice'),
]
