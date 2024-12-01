from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from Cart.cart import Cart

@receiver(user_logged_out)
def save_cart_on_logout(sender, request, user, **kwargs):
    if request.user.is_authenticated:
        cart = Cart(request)
        print("from save_cart")
        
        cart.save_to_db()  # Save the session cart to the database
        print("saved")
        cart.clear()  # Clear the session cart after saving

@receiver(user_logged_in)
def load_cart_on_login(sender, request, user, **kwargs):
    if request.user.is_authenticated:
        cart = Cart(request)
        cart.load_from_db()  # Load the cart items from the database
