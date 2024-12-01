from django.db import models
from ecommerce.models import Customuser
from ecommerce.models import Product
from django.db.models.signals import  pre_save
from django.dispatch import receiver 
import datetime

class ShippingAddress_Info(models.Model):
    user =  models.ForeignKey(Customuser, on_delete = models.CASCADE)
    shipping_full_name  = models.CharField(max_length=255)
    shipping_email =  models.CharField(max_length=255)
    shipping_address1  = models.CharField(max_length=255)
    shipping_address2  = models.CharField(max_length=255,null=True,blank=True)
    shipping_city =  models.CharField(max_length=255)
    shipping_state =  models.CharField(max_length=255, null = True ,blank=True)
    shipping_zipcode =  models.CharField(max_length=255, null=True,blank=True)
    shipping_country =  models.CharField(max_length=255)
    class Meta:
        verbose_name_plural =  "Shipping Address"
    def __str__(self):
        return f'Shipping Address {str(self.id)}'


class Order(models.Model):
	user = models.ForeignKey(Customuser, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=250)
	email = models.EmailField(max_length=250)
	shipping_address = models.TextField(max_length=15000)
	amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
	date_ordered = models.DateTimeField(auto_now_add=True)	
	shipped = models.BooleanField(default=False)
	date_shipped = models.DateTimeField(blank=True, null=True)
	
	def __str__(self):
		return f'Order - {str(self.id)}'


# Auto Add shipping Date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
	if instance.pk:
		now = datetime.datetime.now()
		obj = sender._default_manager.get(pk=instance.pk)
		if instance.shipped and not obj.shipped:
			instance.date_shipped = now

# Create Order Items Model
class OrderItem(models.Model):
	# Foreign Keys
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(Customuser, on_delete=models.CASCADE, null=True, blank=True)

	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	is_shipped = models.BooleanField(default=False)


	def __str__(self):
		return f'Order Item - {str(self.id)}'