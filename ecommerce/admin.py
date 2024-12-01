from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Seller)
from ecommerce.models import Customuser
  

#inline will show another model after one model
class ProfileInline(admin.StackedInline):
    model = Profile
class UserAdmin(admin.ModelAdmin):
    model = Customuser
    list_display = ('email', 'role', 'is_active', 'is_staff')  # Include role in list view
    fields = ['username', 'email', 'groups', 'password', 'role', 'is_active', 'is_staff']  # Include role in form
    inlines = [ProfileInline]  # Add Profile inline admin

# Register the Customuser model with UserAdmin
admin.site.register(Customuser, UserAdmin)

