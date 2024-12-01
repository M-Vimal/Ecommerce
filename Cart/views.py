from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from ecommerce.models import Product
from django.contrib import messages
# Create your views here.
def cart(request):
    cart = Cart(request)
    cart_items = cart.get_prods
    product_quantities = cart.get_quants
    total = cart.total()
    return render(request,'cart/cart.html',{'cart_items':cart_items,'product_qty':product_quantities,'total_amount':total})

def add_cart(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id =  int(request.POST.get('product_id'))
        quantity =  int(request.POST.get('product_qty'))

        #lookup product in DB
        product = get_object_or_404 (Product, id= product_id)
        # Save to session
        cart.add(product=product,quantity=quantity)
        cart_quantity = cart.__len__()
        msg = "product successfully added to cart"
        response = JsonResponse({'qty':cart_quantity})
        messages.success(request,msg)
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id =  int(request.POST.get('product_id'))
        quantity =  int(request.POST.get('product_qty'))
        cart.update(product=product_id,quantity=quantity)
        response = JsonResponse({'msg':'cart has been successfully updated'})
        messages.success(request,'cart has been successfully updated')
        return response
    
 

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id =  int(request.POST.get('product_id'))
        cart.delete(product_id)
        response = JsonResponse({'msg':"successfully deleted"})
        messages.success(request,'item removed from cart')

        return response
        #return JsonResponse({"msg":"successfully removed"})
