from django.contrib import messages
from core.forms import ProductForm
from django.shortcuts import render, redirect
from core.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

import razorpay

from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html',{'products':products})



def product(request):
    products = None
    shop = Shop.objects.all()
    shopid = request.GET.get('shop')
    filter_price = Filter_Price.objects.all()
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    elif shopid:
        products = Product.objects.filter(shop = shopid)
    else:
        products = Product.objects.all()
    data = {}
    data['products'] = products
    data['categories'] = categories
    data['shop'] = shop
    data['filter_price'] = filter_price
    return render(request, 'core/product.html',data)

def search(request):
    shop = Shop.objects.all()
    shopid = request.GET.get('shop')
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    filter_price = Filter_Price.objects.all()
    query = request.GET['query']
    product = Product.objects.filter(name__icontains = query)
    context = {
        "product":product,
        "shop":shop,
        "categories":categories,
        "filter_price":filter_price,
    }
    return render(request,'core/search.html',context)



def contact(request):
    if request.method == 'POST':
        contact = Contact_us(
            name = request.POST.get('name'),
            subject = request.POST.get('subject'),
            email = request.POST.get('email'),
            company_name = request.POST.get('company_name'),
            message = request.POST.get('message'),
        )
        contact.save()
    return render(request, 'core/contact.html')

@login_required(login_url= "/accounts/user_login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("product")


@login_required(login_url="/accounts/user_login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/user_login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/user_login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/user_login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/user_login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def checkout(request):
    payment = client.order.create({
        "amount": 500,
        "currency": "INR",
        "payment_capture":"1"
         })

    order_id = payment['id']
    context = {
        'order_id' : order_id,
        'payment' : payment,
    }

    return render(request, 'cart/checkout.html',context)


def place_order(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')

        firstname = request.POST.get('firstname')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        amount = request.POST.get('amount')


        context = {
            'order_id':order_id,
        }

        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            city = city,
            address = address,
            pincode = pincode,
            email = email,
            phone = phone,
            payment_id = order_id,
            amount = amount,
        )
        order.save()



        return render(request, 'cart/placeorder.html',context)
