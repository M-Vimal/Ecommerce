from django.shortcuts import render,redirect
from Cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress_Info
from django.contrib import messages
from .models import Order,OrderItem
from ecommerce.models import Product,Seller
from payment.models import Order,OrderItem

#paypal integration
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

# display shipped items for particular seller (sellers only)
def shipped_dash(request):
    if request.user.is_authenticated:
        if request.user.role == 'seller':
            # retrive the seller
            seller = Seller.objects.get(seller_name_id = request.user.id)
            order_items = OrderItem.objects.filter(product__seller = seller) # '__' usedto search across multiple models.it retrive particular seller product only
            shipped_products = []
            for item in order_items:
                if item.is_shipped:
                    shipped_products.append(item)

            if shipped_products:
                return render(request,'payment/shipped_dash.html',{'shipped_products':shipped_products}) 
            else:
                messages.success(request,'No shipped products')
                return render(request, 'payment/shipped_dash.html', {'shipped_products': []})
        else:
            messages.success(request,"you are not a seller")
            return redirect('home')
    else:
        messages.success(request,"Access Denied")
        redirect('home')

def unshipped_dash(request):
    if request.user.is_authenticated:
        if request.user.role == 'seller':
            seller = Seller.objects.get(seller_name_id = request.user.id)
            order_items = OrderItem.objects.filter(product__seller = seller)
            unshipped_products = []
            for item in order_items:
                if not item.is_shipped:
                    unshipped_products.append(item)
            print(unshipped_products)

            if unshipped_products:
                return render(request,'payment/unshipped_dash.html',{'unshipped_products':unshipped_products})
            else:
                messages.success(request,'0 Unshipped products')
                return render(request, 'payment/unshipped_dash.html', {'unshipped_products': []})
        else:
            messages.success(request,"you are not a seller")
            return redirect('home')
    else:
        messages.success(request,"Access Denied")
        return redirect('home')

def update_shipped_status(request,pk):
    if request.user.is_authenticated:
        if request.user.role == 'seller':
            seller = Seller.objects.get(seller_name_id = request.user.id)
            if request.user.id == seller.seller_name.id:
                if request.method == 'POST':
                    #retrive orderitem
                    orderitem = OrderItem.objects.get(id=pk)
                    #change status to shipped
                    orderitem.is_shipped = True
                    orderitem.save()
                    return redirect('unshippeddash')
            else:
                messages.success(request,"it  not your product")
                return redirect('home')
        else:
            messages.success(request,"access denied")
            return redirect('home')
    else:
        messages.success(request,"please login")
        return redirect('login')
    
            

def process_order(request):
    if request.POST:
        if request.user.is_authenticated:
            pamentinfo = PaymentForm(request.POST or None)
            my_shipping = request.session.get('my_shippinginfo')
            cart = Cart(request)
            cart_items = cart.get_prods()   #if we use this in template we dont need to call it .just refer it 'get_prods'
            product_quantities = cart.get_quants()
            total = cart.total()
            print('from procss',cart_items,'q=',product_quantities)

            #order info
            full_name = my_shipping['shipping_full_name']
            email = my_shipping['shipping_email']
            user=request.user
            shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"

            create_order = Order(user=user,email=email,full_name = full_name,shipping_address = shipping_address,amount_paid = total)
            create_order.save()


            #orderitem info
            for product in cart_items:
                print(product)
                product_id = product.id
                quantity = product_quantities[str(product_id)]
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                oreder_item = OrderItem(order=create_order,product=product,quantity=quantity,price=price,user=user)
                oreder_item.save()
            #delete the session, we create to store cart to empty our cart 
            for key in request.session.keys():
                print("delete key:",key)
                if key == "session_key":
                    del request.session[key]
                    break
            print("keys",request.session.keys())
            messages.success(request,'order placed')
            return redirect('home')
        else:
            messages.success(request,'restricted page')
            return redirect('home')
    else:
        messages.success(request,'access denied')
        return redirect('home')

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_items = cart.get_prods
        product_quantities = cart.get_quants
        total = cart.total()

        #get host
        host = request.get_host()

        #for payapl payment
        paypal_dict = {
        "business": 'test2@businessgmail.com',
        "amount": total,
        "item_name": "sticker",
        "invoice": str(uuid.uuid4()),
        "notify_url": 'http://{}{}'.format(host,reverse('paypal-ipn')),
        "return_url": 'http://{}{}'.format(host,reverse('payment_success')),
        "cancel_return": 'http://{}{}'.format(host,reverse('payment_failed')),
        }

        # Create the instance.
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)


        if request.user.is_authenticated:
            shippinginfo = request.POST
            #this session remain until new order override this session
            request.session['my_shippinginfo']=shippinginfo
            #for credit card payment
            paymentform = PaymentForm()
            return render(request,'payment/billing_info.html',{'paypal_form':paypal_form,'cart_items':cart_items,'product_qty':product_quantities,'total_amount':total,'shippinginfo':shippinginfo,'paymentform':paymentform})
        else:
            messages.success(request,'access denied.login')
            return redirect('login')
    else:
        messages.success(request,'access denied')
        redirect('home')



def checkout(request):
    cart = Cart(request)
    cart_items = cart.get_prods
    product_quantities = cart.get_quants
    total = cart.total()
    if request.user.is_authenticated:
        shipping_user = ShippingAddress_Info.objects.get(user = request.user)
        shippingform = ShippingForm(request.POST or None,instance=shipping_user)
        return render(request,'payment/checkout.html',{'cart_items':cart_items,'product_qty':product_quantities,'total_amount':total,'shippingform':shippingform})
    else:
        messages(request,'please login')
        return redirect('login')


def payment_success(request):
    return render(request,'payment/payment_success.html')

def payment_failed(request):
    return render(request,'payment/payment_failed.html')