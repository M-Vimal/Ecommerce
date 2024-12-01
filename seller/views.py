from django.shortcuts import render,redirect
from .forms import AddproductForm
from django.contrib import messages
from ecommerce.models import Seller
def add_product(request):
    if request.user.is_authenticated:
        if request.user.role == 'seller':
            seller = Seller.objects.get(seller_name_id = request.user.id)
            if request.method == 'POST':
                print(request.POST)
                if seller.seller_name.id == request.user.id:
                    print(request.FILES)
                    new_product = AddproductForm(request.POST ,request.FILES)
                    print(new_product)
                    if new_product.is_valid():
                        product = new_product.save(commit=False)
                        product.seller = seller  # product needs to be linked to seller
                        product.save()
                        messages.success(request, 'Product added successfully!')
                        return redirect('home')
                    else:
                        for error in new_product.errors.get('__all__', []):  # `__all__` is used to capture non-field errors
                            messages.error(request, error)
                else:
                    messages(request,"you seller id doesnot match.")
        form = AddproductForm

        return render(request,'seller/add_product.html',{'form':form})
    else:
        messages(request,"please login to add product")
        return redirect('login')
