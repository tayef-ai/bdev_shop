from django.shortcuts import render, redirect
from .models import Product, Cart, OrderPlaced, Customer, Category
from .forms import CustomerRegistrationForm, CustomerProfileForm, ContactForm, SearchForm, CustomerAddressForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def homeview(request):
    latest_product = Product.objects.all().order_by('-id')[:6]
    popular_product = Product.objects.all()[:6]
    categories = Category.objects.all()[:6]
    context = {
        'latest_product': latest_product,
        'popular_product': popular_product,
        'categories': categories,
    }
    return render(request, 'ecomapp/home.html', context)

def aboutusview(request):
    return render(request, 'ecomapp/aboutus.html')

def contactview(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Message has been sent Successfully!!")
            form = ContactForm()
            HttpResponseRedirect('/')
    else:
        form = ContactForm()
    return render(request, 'ecomapp/contact.html', {'form': form})

def latestproductview(request):
    if request.GET.get('category'):
        category2 = request.GET.get('category')
        print("category2", category2)
        category = Category.objects.get(pk=int(category2))
        print("MYcat00000", category)
        if request.GET.get('l2h'):  
            
            products = Product.objects.filter(category=category).order_by('discounted_price','selling_price')
            print("MYprod111111111", products)
        else:
            products = Product.objects.filter(category=category).order_by('-discounted_price','-selling_price')
        return render(request, 'ecomapp/allproducts.html', {'products': products, 'catid': category2})
    elif request.GET.get('l2h'):
        products = Product.objects.order_by('discounted_price','selling_price')
    elif request.GET.get('h2l'): 
        products = Product.objects.order_by('-discounted_price', '-selling_price')
    else:
        products = Product.objects.all().order_by('-id')
    return render(request, 'ecomapp/allproducts.html', {'products': products})

def popularproductview(request):
    products = Product.objects.all()
    return render(request, 'ecomapp/allproducts.html', {'products': products})

def categoryview(request):
    categories = Category.objects.all()
    return render(request, 'ecomapp/allproducts.html', {'categories': categories})

def cateproductsview(request, id):
    category = Category.objects.get(pk=id)
    print("_____________", category)
    products = Product.objects.filter(category=category)
    return render(request, 'ecomapp/allproducts.html', {'products': products, 'catid': id})

def productdetailview(request, id):
    product = Product.objects.get(pk=id)
    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'ecomapp/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'ecomapp/register.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations!! Registration Successful.")
            form.save()
            form = CustomerRegistrationForm()
        return redirect('/login/')

@login_required    
def seeprofile(request):
    return render(request, 'ecomapp/profile.html')

@method_decorator(login_required, name='dispatch')
class EditProfileview(View):
    def get(self, request):
        form = CustomerProfileForm(instance=request.user)
        return render(request, 'ecomapp/editprofile.html', {'form':form})
    def post(self, request):
        predata = User.objects.get(id=request.user.id)  
        form = CustomerProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            un = form.cleaned_data['username']
            fn = form.cleaned_data['first_name']
            ln = form.cleaned_data['last_name']
            em = form.cleaned_data['email']
            predata.username = un
            predata.first_name = fn
            predata.last_name = ln
            predata.email = em
            predata.save()
            # form.save()
            # profile = form.save(commit=False)
            # profile.user = request.user
            # profile.save()
            # print("User======", request.user)
            # reg = Customer(user=request.user, shipping_address = sa, phone = ph)
            # print("reg========", reg)
            # reg.save()
            messages.success(request, "Congratulations!!! Profile Updated Successfully.")
        return HttpResponseRedirect('/seeprofile/')

@method_decorator(login_required, name='dispatch')
class EditProfileview2(View):
    def get(self, request):
        form = CustomerAddressForm(instance=request.user.customer)
        return render(request, 'ecomapp/editprofile2.html', {'form':form})
    def post(self, request):
        form = CustomerAddressForm(request.POST, instance=request.user.customer)
        if form.is_valid():
            form.save()
            # profile = form.save(commit=False)
            # profile.user = request.user
            # profile.save()
            # print("User======", request.user)
            # reg = Customer(user=request.user, shipping_address = sa, phone = ph)
            # print("reg========", reg)
            # reg.save()
            messages.success(request, "Congratulations!!! Profile Updated Successfully.")
        return HttpResponseRedirect('/seeprofile/')
@login_required
def addtocart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    prod_exist = Cart.objects.filter(user=user, product=product).exists()
    if prod_exist:
        return redirect('/cart/')
    else:
        Cart(user=user, product=product).save()
    return redirect('/cart/')

@login_required
def show_cart(request):
    user = request.user
    carts = Cart.objects.filter(user=user).order_by('-id')
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
        total_amount = amount + shipping_amount
    return render(request, 'ecomapp/addtocart.html', {'carts': carts, 'totalamount': total_amount, 'amount': amount})

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount += tempamount
            total_amount = amount + shipping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': total_amount,
            }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount += tempamount
            total_amount = amount + shipping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': total_amount,
            }
        return JsonResponse(data)
    
@login_required
def remove_cart(request, id):
    if request.method == 'GET':
        # prod_id = request.GET['pid']
        prod_id = id
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }
        # return JsonResponse(data)
        return redirect('/cart/')
    
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
        total_amount = amount + shipping_amount
    return render(request, 'ecomapp/checkout.html', {'add': add, 'totalamount': total_amount, 'cartitems': cart_items})

@login_required
def payment_done(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    if not customer.shipping_address or not customer.phone:
        messages.warning(request, "Please Provide Your Address and Moble No. To Confirm Order")
        return redirect('/seeprofile/')
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    messages.success(request, "Your Order has been Placed Successfully.")
    return redirect("orders")

@login_required
def orders(request):
    customer = Customer.objects.get(user=request.user)
    op = OrderPlaced.objects.filter(customer=customer).order_by('-id')
    return render(request, 'ecomapp/orders.html', {'order_placed': op})

@login_required
def cancelorder(request, id):
    op = OrderPlaced.objects.get(id=id)
    op.delete()
    messages.warning(request, "Your Order has been cancelled Successfully.")
    return redirect("/orders/")

def SearchView(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            categories = Category.objects.filter(categoryname__icontains=query)
            print("Cat======", categories)
            print("pro=======", products)
            return render(request, 'ecomapp/allproducts.html', {'products': products, 'categories': categories})
    return render(request, 'ecomapp/allproducts.html', {'products': None, 'categories': None})

    
