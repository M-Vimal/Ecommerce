from django.conf import settings
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from payment.models import Order

@receiver(valid_ipn_received)
def paypal_payment_received(sender,**kwargs):
    obj = sender
    print(obj)
    print(f"amount {obj.mc_gross}")

