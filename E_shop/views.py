from django.shortcuts import render,redirect
from store_app.models import Product, Categories, Contact_us, Order, OrderItem
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
import razorpay
from math import ceil

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRECT))

def BASE(request):
    return render(request,'main/base.html')

def HOME(request):

    product = Product.objects.filter(status='PUBLISH')
    #n = len(product)
    #nSlides = n // 4 + ceil((n / 4) + (n // 4))
    context = {
        'product': product
    }
    return render(request,'main/index.html',context)

def PRODUCT(request):
    product = Product.objects.filter(status='PUBLISH')
    categories = Categories.objects.all()

    CATID = request.GET.get('categories')
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')
    if CATID:
        product = Product.objects.filter(categories=CATID)
    elif ATOZID:
        product = Product.objects.filter(status='PUBLISH').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='PUBLISH').order_by('-name')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status='PUBLISH',condition='New').order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status='PUBLISH',condition='New').order_by('id')
    else:
        product = Product.objects.filter(status='PUBLISH').order_by('-id')


    context = {
        'product': product,
        'categories' : categories,

    }
    return render(request,'main/product.html',context)

def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains= query)
    context = {
        'product': product
    }
    return render(request,'main/search.html',context)

def PRODUCT_DETAILS(request,id):
    prod = Product.objects.filter(id = id).first()
    context = {
        'prod' : prod
    }
    return render(request,'main/product_details.html',context)

def CONTACT_US(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()
        return redirect('home')

    return render(request,'main/contact.html')

def about(request):
    return render(request,'main/about.html')

def HandleRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')

    return render(request,'Registration/auth.html')

def HandleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'Registration/auth.html')

def HandleLogout(request):
    logout(request)
    return redirect('home')
    #return render(request, 'main/index.html')

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect('cart_detail')

@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")

@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_details.html')

def CHECK_OUT(request):
    amount_str = request.POST.get('amount')
    amount_float = float(amount_str)
    amount = int(amount_float)*100

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })
    order_id = payment['id']
    context = {
        'order_id': order_id,
        'payment': payment,
    }
    return render(request,'cart/checkout.html', context)
def PLACE_ORDER(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        context = {
            'order_id':order_id,
        }

        order = Order (
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            city = city,
            address = address,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount,
        )
        order.save()

        for i in cart:
            a = cart[i]['quantity']
            b = int(cart[i]['price'])
            total = a * b

            item = OrderItem (
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total,
            )
            item.save()
        return render(request,'cart/placeorder.html', context)


@csrf_exempt
def SUCCESS (request):
    if request.method=="POST":
        a = request.POST
        order_id = ''
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Order.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
    return render(request,'cart/thankyou.html',)

@login_required(login_url="/login/")
def profileview(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    order = Order.objects.filter(user=user)
    context = {
        'order': order,
    }
    print(context)

    return render(request,'main/profileview.html',context)


