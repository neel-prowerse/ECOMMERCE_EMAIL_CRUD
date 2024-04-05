from django.shortcuts import render,redirect
from .models import Mobile,Company,Cart, Order
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm,MobileForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
# Create your views here.

# This is index it consists of dropdown logic
def index(request): 
    company = Company.objects.all()
    return render(request,'index.html',{'company':company})

# This is add it consists of Creating or Adding a new product.
def add(request):
    if request.method  == 'POST':
        form = MobileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/show/')
    else:
        form = MobileForm()
        return render(request, 'add.html',{'form':form})
    
# Modify the add_to_cart function
@login_required
def add_to_cart(request, id):
    if request.user.is_authenticated:
        mobile = get_object_or_404(Mobile, id=id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, mobile=mobile)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        # Redirect to index after adding to cart
        return redirect('/show/')
    else:
        # If user is not logged in, redirect to the login page
        return redirect('loginaccount')
    
@login_required
def remove_from_cart(request, mobile_id):
    # Get the cart item to be removed
    cart_item = get_object_or_404(Cart, user=request.user, mobile_id=mobile_id)
    # Delete the cart item
    cart_item.delete()
    # Redirect back to the checkout page or any other appropriate page
    return redirect('checkout') 

# Modify the checkout function
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.mobile.Price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})
# Modify the index function to display add to cart buttons

def order_confirmation(request):
    return render(request, 'order_confirmation.html')


# Modify the confirm_checkout function
def confirm_checkout(request):
    if request.method == 'POST':
        # Retrieve shipping information from the form
        # ... (Remaining code as before)

        # Redirect to order confirmation page
        return redirect('order_confirmation')
    else:
        # If not a POST request, redirect to checkout page
        return redirect('checkout')

# This is show logic it shows all products
def show(request):
    searchTerm = request.GET.get('searchTerm')
    if searchTerm:
        mobiles = Mobile.objects.filter(company__name__contains=searchTerm)
    else:
        mobiles = Mobile.objects.all()
    return render(request,'show.html',{'mobiles':mobiles, 'searchTerm':searchTerm})

# This is showid it shows one specific item by its id
def showid(request,id):
    company = Company.objects.filter(id=id)
    mobile = Mobile.objects.filter(id=id)
    return render(request,'mobile.html',{'mobile':mobile,'company':company})

# This is edit logic for editing an existing product
def edit(request,id):
    mobile = Mobile.objects.get(id=id)
    return render(request,'edit.html',{'mobile':mobile})

# This is update logic for editing an existing product
def update(request, id):
    mobile = Mobile.objects.get(id=id)
    if request.method == 'POST':
        form = MobileForm(request.POST, request.FILES, instance=mobile)
        if form.is_valid():
            form.save()
            return redirect('/show/')  # Redirect to the Show URL after saving
    else:
        form = MobileForm(instance=mobile)
    return render(request, 'edit.html', {'mobile': mobile, 'form': form})

# This is delete logic for deleting an existing product
def delete(request, id):
    mobile = Mobile.objects.get(id=id)
    mobile.delete()
    return redirect('show')

# This is register logic through this we can register or sign-up
def register(request):
    if request.method == 'GET':
        return render(request,'register.html',{'form':UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('loginaccount')
            except IntegrityError:
                return render(request,'register.html',{'form':UserCreateForm,'error':'Username already exists.'})
        else:
            return render(request,'register.html',{'form':UserCreateForm,'error':'Passwords do not match'})

# This is login logic through this we can login or sign-in
def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'login.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request, username = request.POST['username'],password = request.POST['password'])
        if user is None:
            return render(request, 'login.html',{'form':AuthenticationForm(),'error':'username and password do not match'})
        else:
            login(request,user)
            return redirect('index')

# This is logout logic through this we can logout or if user is already logout it will show error message.
@login_required
def logoutaccount(request):
    logout(request)
    return redirect('index')






