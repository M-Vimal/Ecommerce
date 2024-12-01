from urllib import response
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from .forms import LoginForm,RegisterForm,Update_user_profile,Changepassword,UserInfoForm
from django.contrib import messages
from .models import Customuser,Product,Category,Profile
from django.contrib.auth.models import Group
from payment.models import ShippingAddress_Info,Order,OrderItem
from payment.forms import ShippingForm


def homeview(request):
    # search product 
    if request.method == 'POST':
        searched = request.POST.get('search_value')
        print(searched)
        if searched != 'None':
            products = Product.objects.filter(p_name__icontains = searched)
            if len(products) <= 0:
                return render(request,'account/home.html',{'msg':"sorry,we dont have that product"})
            return render(request,'account/home.html',{'products':products})
        else:
            products = Product.objects.all()
            return render(request,'account/home.html',{'products':products})
    # display all products
    products = Product.objects.all()
    return render(request,'account/home.html',{'products':products})

# to show particular product
def productview(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'account/product.html',{'product':product})

def aboutview(request):
    return render(request,'account/about.html')

# show product base on their catagory
def categoryview(request,foo):  
    category = Category.objects.get(name = foo)
    products = Product.objects.filter(category=category)
    context = {"products":products,"category":category}
    return render(request,'account/category.html',context)


def loginview(request):
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid(): 
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user is not None:
                login(request,user)
                print("successfully login")
                return redirect('home')
            else:
                print("invalid crendtials")
                messages.error(request,"invalid credentials")


    return render(request,'account/login.html',{'loginform':LoginForm})


def signupview(request):
    regform = RegisterForm()
    if request.method == "POST":
        print(request)
        regform = RegisterForm(request.POST)
        if regform.is_valid():
            user = regform.save(commit=False)  # Save without committing to hash password
            user.set_password(regform.cleaned_data['password'])  # Hash password explicitly
            user.save()
            role = request.POST.get('role')
            print(role)
            if role == 'Customer':
                group = Group.objects.get(name='customer')
                group.user_set.add(user)
            elif role == 'Seller':
                group = Group.objects.get(name='seller')
                group.user_set.add(user)
            email = regform.cleaned_data['email']
            password = regform.cleaned_data['password']
            
            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Account created successfully")
                return redirect('updateinfo')
            else:
                messages.error(request, "Authentication failed. Please check your email and password.")

    return render(request,'account/signup.html',{'registerform':regform})


def update_profile(request):
    if request.user.is_authenticated:
        login_user = Customuser.objects.get(id=request.user.id)

        user_update_form = Update_user_profile(request.POST or None, instance=login_user)
        if user_update_form.is_valid():
            login_user.save()
            login(request,login_user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,"profile updated successfully")
            return redirect('home')
        return render(request,'account/update_profile.html',{'user_update_form':user_update_form})
    else:
        messages.success(request,"you must logged in to access that page ")
        return redirect('home')


def update_password(request):
        if request.user.is_authenticated:
            login_user = request.user
            if request.method == "POST":
                password_update_form = Changepassword(login_user,request.POST)
                if password_update_form.is_valid():
                    login_user.save()
                    messages.success(request,'password changed')
                    login(request,login_user,backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home')
                else:
                    for error in list(password_update_form.errors.values()):
                        messages.error(request,error)
                        return redirect('updatepassword')
            else:
                password_update_form = Changepassword(login_user)
                return render(request,'account/update_password.html',{'password_update_form':password_update_form})
        else:
            messages.success(request,"you must logged in to access that page")
            return redirect('home')



def update_info(request):
    if request.user.is_authenticated:
        login_user = Profile.objects.get(user__id = request.user.id)
        shipping_user, created = ShippingAddress_Info.objects.get_or_create(user=request.user)
        print("shipping user id",shipping_user)
        update_infoform = UserInfoForm(request.POST or None,instance = login_user)
        shippingform = ShippingForm(request.POST or None,instance=shipping_user)
        if update_infoform.is_valid() or shippingform.is_valid():
            update_infoform.save()
            shippingform.save()
            messages.success(request,"profile updated successfully")
            return redirect('home')
        return render(request,'account/update_info.html',{'update_infoform':update_infoform,'shippingform':shippingform})
    else:
        messages.success(request,"you ont have access to that page")
        return redirect('home')
        


# to change status of order
def order_shipped_status(request,pk):
    if request.method == 'POST':
        print(request.POST)
        order = Order.objects.get(id=pk)
        order.shipped = True
        order.save()
        return redirect('allorders')




# display all order(for only admin).
def all_orders(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            allorders = Order.objects.all()
            return render(request,'account/allorder.html',{'allorders':allorders})
        else:
            messages(request,"please login with your admin account")
            return redirect('login')
    else:
        messages(request,"access denied")
        return redirect('home')

# display orderitems particular order
def order_details(request,pk):
    orderdetails = OrderItem.objects.filter(order_id = pk)
    return render(request,'account/allorder.html',{'orderdetails':orderdetails})




    
#to show their orders
def my_orders(request):
    if request.user.is_authenticated:
        myorders = Order.objects.filter(user__id = request.user.id)
        print(myorders)
        print(request.user.id)
        return render(request,'account/myorders.html',{'myorders':myorders})
    else:
        messages(request,"access denied")
        return redirect('home')
    