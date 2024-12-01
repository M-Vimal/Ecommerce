from django.contrib import admin
from django.urls import path
from .views import *



urlpatterns = [
    path('addproduct/',add_product,name="addproduct"),


]