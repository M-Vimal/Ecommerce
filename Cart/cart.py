from ecommerce.models import Product
from Cart.models import CartItem
class Cart:
    def __init__(self,request):
        self.session = request.session
        self.request = request

        #this will retrive the  session named 'cart'.if there is no 'cart' in session create a an empty sessionkey named 'cart'  . 
        self.cart = self.session.setdefault('cart', {})

    def save(self):
        """Save the cart to the session and mark session as modified."""
        self.session['cart'] = self.cart
        self.session.modified = True 


    def total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for product in products:
            quantity = self.cart.get(str(product.id), 0)
            if product.sale_price:
                total += product.sale_price * quantity
            else:
                total += product.price * quantity
        return total
        
    def add(self,product,quantity):
        product_id = str(product.id) 
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.save()
        


    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        prod_ids = self.cart.keys()
        products = Product.objects.filter(id__in = prod_ids)
        return products
    def get_quants(self):
        quantities = self.cart
        return quantities
    def update(self,product,quantity):
        cart = self.cart
        productid = str(product)
        productquantity = int(quantity)
        cart[productid] = productquantity
        self.save()
        ourcart = self.cart
        return ourcart
    
    def delete(self,product):
        cart=self.cart
        productid = str(product)
        cart.pop(productid)
        self.save()
        ourcart = self.cart
        return ourcart
    
    def save_to_db(self):
        """Save the cart items to the database."""
        user = self.request.user
        print(self.cart)
        for product_id, quantity in self.cart.items():
            product = Product.objects.get(id=int(product_id))

            CartItem.objects.update_or_create(
                user=user,
                product=product,
                defaults={'quantity': quantity}
            )

    def load_from_db(self):
        """Load cart items from the database into the session."""
        cart_items = CartItem.objects.filter(user=self.request.user)
        print(cart_items)
        for item in cart_items:
            self.cart[item.product_id] = item.quantity
        self.save()

    def clear(self):
        """Clear cart from both session and database."""
        self.cart = {}
        self.save()




