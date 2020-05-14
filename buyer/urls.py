from django.urls import path

from .views import *

app_name = 'buyer'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='buyer-dashboard'),
]
