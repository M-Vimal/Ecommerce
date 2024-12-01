from django.db import models
from ecommerce.models import Product,Customuser

from django.conf import settings

class CartItem(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assume you have a Product model
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.p_name} x {self.quantity}"
