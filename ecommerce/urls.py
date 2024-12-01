from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('',homeview,name="home"),
    path('login/', loginview,name="login"),
    path('signup/',signupview,name="signup"),
    path('updateprofile/',update_profile,name="updateprofile"),
    path('updateinfo/',update_info,name="updateinfo"),
    path('updatepassword/',update_password,name="updatepassword"),
    path('about/',aboutview,name="about"),
    path('product/<int:pk>',productview,name="product"),
    path('category/<str:foo>',categoryview,name="category"),
    path('allorders/',all_orders,name="allorders"),
    path('order/<int:pk>',order_details,name="orderdetails"),
    path('order_shipped_status/<int:pk>',order_shipped_status,name="ordershippedstatus"),
    path('myorders/',my_orders,name="myorders"),

]