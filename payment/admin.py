from django.contrib import admin
from .models import ShippingAddress_Info,Order,OrderItem
# Register your models here.
admin.site.register(ShippingAddress_Info)
admin.site.register(OrderItem)
admin.site.register(Order)


class orderitem(admin.StackedInline):
    model = OrderItem
    extra = 0  #if we not give extra .it show empty orderitem object for future orderitems.
    
class Orders_with_OrderItem(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [orderitem]

admin.site.unregister(Order)
admin.site.register(Order,Orders_with_OrderItem)
