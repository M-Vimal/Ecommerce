from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('cart/',cart,name="cart"),
    path('addcart/',add_cart,name="addcart"),
    path('updatecart/',cart_update,name="updatecart"),
    path('deleteitem/',cart_delete,name="deleteitem"),

]