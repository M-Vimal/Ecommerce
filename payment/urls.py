from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('payment_success',payment_success,name="payment_success"),
    path('payment_failed',payment_failed,name="payment_failed"),
    path('checkout',checkout,name="checkout"),
    path('billinginfo',billing_info,name="billinginfo"),
    path('processorder',process_order,name="processorder"),
    path('shippeddash',shipped_dash,name="shippeddash"),
    path('unshippeddash',unshipped_dash,name="unshippeddash"),
    path('update_shipped_status/<int:pk>',update_shipped_status,name='update_shipped_status'),
    path('paypal',include('paypal.standard.ipn.urls')),
]