from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/staff')
        else:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, iscompleted=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all();
    CropTopProduct = Product.objects.filter(category="Crop Top")
    PantsProduct =  Product.objects.filter(category="Pant")
    JactketProduct = Product.objects.filter(category="Jacket")
    ShoesProduct = Product.objects.filter(category="Shoes")
    Sportequipment = Product.objects.filter(category="Sport equipment")
    context= {'products': CropTopProduct, 'PantsProduct': PantsProduct,'JactketProduct':JactketProduct, 'Sportequipment':Sportequipment,'ShoesProduct': ShoesProduct, 'cartItems':cartItems}
    return render(request, "store/store.html", context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, iscompleted=False)
        items = order.orderitem_set.all()
        if order.get_cart_total < 1:
            cartItems = order.get_cart_items
            context = {'items': items, 'order': order, 'cartItems': cartItems, "noitem": True}
            return render(request, 'store/cart.html', context)
        else:
            cartItems = order.get_cart_items
            if request.method == 'POST':
                receiver_phone = request.POST.get('receiver_phone')
                city = request.POST.get('city')
                receiver_name = request.POST.get('receiver_name')
                address = request.POST.get('address')
                paymentmethod = request.POST.get('paymentmethod')
                order_date = request.POST.get('order_date')
                print('checkout information: receiver_name:', receiver_name, 'receiver_phone:', 'order_date:', order_date, receiver_phone, 'city:', city, 'address:', address, 'paymentmethod:', paymentmethod)
                if ShippingInformation.objects.filter(customer=customer, order=order).exists():
                    shipping = ShippingInformation.objects.get(customer=customer, order=order)
                else:
                    shipping, created = ShippingInformation.objects.get_or_create(customer=customer, order=order, city=city, address=address, order_date=order_date, phone=receiver_phone)
                payment, created = Payment.objects.get_or_create(customer=customer, order=order, method=paymentmethod)
                order.iscompleted=True
                order.save()
                if paymentmethod == 'COD':
                    shipping.status = 'New'
                    shipping.save()
                    payment.payment_factory
                if paymentmethod == 'VNPAY':
                    payment.payment_factory
                    shipping.status = 'New'
                    shipping.save()
                context = {'iscompleted': order.iscompleted}
                return render(request, 'store/checkout.html', context)
            context = {'items': items, 'order': order, 'cartItems': cartItems}
            return render(request, 'store/checkout.html', context)
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        items = []
        return redirect("login")


def loginForCustomer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/staff')
            else:
                return redirect('/')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, "store/registration/login.html", context)


def register(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created' + user)
            return redirect('login')
    else:
        form = CustomerForm()
    return render(request, 'store/registration/register.html', {'form': form})


def logoutForCustomer(request):
    logout(request)
    return redirect('/')

def customerprofile(request):
    if request.user.is_authenticated:
        user = request.user
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,iscompleted = False)
        all_shipping = ShippingInformation.objects.filter(customer=customer).order_by('order_date', 'order_date').select_related()
        cartItems = order.get_cart_items
        count_order = all_shipping.count()
        payments = Payment.objects.filter(ispay=True, customer=customer)
        total_spend_money = sum(payment.get_total_price for payment in payments)
    else:
        return redirect("login")
    context = {'user': user, 'cartItems': cartItems, 'total_spend_money': total_spend_money, "all_orders": all_shipping, "count_order": count_order}
    return render(request, 'store/registration/profile.html', context)


def cancel_order(request):
    if request.user.is_authenticated:
        user = request.user
        customer = request.user.customer
        if request.method == "POST":
            data = json.loads(request.body)
            action = data['action']
            shippingid = data['shippingid']
            if action == "CANCEL_ORDER":
                shipping = ShippingInformation.objects.get(customer=customer, id=shippingid)
                shipping.status = "Cancel"
                shipping.save()
                return redirect("customerprofile")
            if action == "CONFIRM_ORDER":
                shipping = ShippingInformation.objects.get(customer=customer, id=shippingid)
                shipping.status = "Delivered"
                shipping.save()
                return redirect("customerprofile")
    else:
        return redirect("login")


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, iscompleted=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        return redirect('login')

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    option = data['option']
    print('Action:', action)
    print('Product:', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, iscompleted=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, option=option)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.delete()
        return redirect('cart')
    elif action == 'change':
        quantity = data['quantity']
        orderItem.quantity = quantity
        if quantity == 0:
            orderItem.delete()
            return redirect('cart')
    elif action == 'changeoption':
        changedoption = data['changedoption']
        if OrderItem.objects.filter(order=order, product=product, option=changedoption).exists():
            data = {'updatesize': False}
            return JsonResponse(data, safe=False)
        else:
            orderItem.option = changedoption
            return redirect('cart')
    orderItem.save()
    if orderItem.quantity == 0:
        orderItem.delete()
        return redirect('cart')
        return JsonResponse('Item was added', safe=False)


def updateEmail(request):
    data = json.loads(request.body)
    email = data['email']
    dob = data['dob']
    phone = data['phone']
    address = data['address']
    user = request.user
    if user.is_authenticated:
        print(email, dob, phone, address)
        customer = user.customer
        user.save()
        user.email = email
        customer.phone = phone
        customer.address = address
        customer.save()
    else:
        return redirect("login")
    return JsonResponse('Update customer info', safe=False)


def detailproduct(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, iscompleted=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    product = Product.objects.get(id=pk)
    comments = product.comment_set.all()
    tags = product.tags.all()
    print(tags)
    context = {'product': product, 'cartItems': cartItems, 'comments': comments, 'tags': tags}
    return render(request, 'store/detailproduct.html', context)


def category(request, name):
    print(name)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, iscompleted=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    if Product.objects.filter(category=name).exists():
        products = Product.objects.filter(category=name)
    else:
        products = Product.objects.filter(tags__name=name)
    print(products)
    context = {'categoryitems': products, 'cartItems': cartItems, 'categoryname': name}
    return render(request, 'store/categoryitems.html', context)

def searchByName(request, productname):
    print(productname)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, iscompleted=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    if Product.objects.get(name=productname).exists():
        products = Product.objects.get(name=productname)
    print(products)
    context = {'categoryitems': products, 'cartItems': cartItems, 'categoryname': productname}
    return render(request, 'store/categoryitems.html', context)


def category_order(request, category):
    all_shipping_by_category = ShippingInformation.objects.filter(status=category).order_by('order_date',
                                                                                 'order_date').select_related()
    print(category)
    context = {'all_shipping_by_category': all_shipping_by_category, 'category': category}
    return render(request, 'store/staff/categoryorder.html', context)

def addcomment(request):
    method = request.method
    customer = request.user.customer
    if method == 'POST':
        data = json.loads(request.body)
        productid = data['productId']
        action = data['action']
        content = data['content']
        print(data)
        print(method)
        product = Product.objects.get(id=productid)
        comment = Comment.objects.create(product=product, customer=customer, content=content)
        print(comment)
    return JsonResponse('Item was added', safe=False)


def addtocart(request):
    user = request.user
    data = json.loads(request.body)
    productid = data['productid']
    if user.is_authenticated:
        if request.method == 'POST':
            customer = user.customer
            action = data['action']
            size = data['size']
            quantity = data['quantity']
            print(customer, action, productid, size, quantity)
            if action == 'addtocart':
                product = Product.objects.get(id=productid)
                order, created = Order.objects.get_or_create(customer=customer, iscompleted=False)
                if OrderItem.objects.filter(order=order, product=product, option=size).exists():
                    orderItem = OrderItem.objects.get(order=order, product=product, option=size)
                    orderItem.quantity = quantity
                    orderItem.save()
                    redirectURL = "product/" + productid
                    return redirect(redirectURL)
                else:
                    orderItem = OrderItem.objects.create(order=order, product=product, option=size, quantity=quantity)
                    return redirect('cart')
        else:
            redirectURL = "product/"+productid
            return redirect(redirectURL)
    return JsonResponse('Item was added', safe=False)


def staff_home(request):
    user = request.user
    if user.is_authenticated:
        all_new_shipping = ShippingInformation.objects.filter(status="New").order_by('order_date',
                                                                                 'order_date').select_related()
        context = {'all_new_shipping': all_new_shipping}
        return render(request, 'store/staff/staffhome.html', context)
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, "store/registration/login.html", context)


def handler_order(request):
    user = request.user
    if user.is_authenticated and user.is_staff:
        if request.method == "POST":
            data = json.loads(request.body)
            action = data['action']
            shippingid = data['shippingid']
            if action == "CANCEL_ORDER":
                shipping = ShippingInformation.objects.get(id=shippingid)
                shipping.status = "Cancel"
                shipping.save()

            if action == "CONFIRM_ORDER":
                shipping = ShippingInformation.objects.get(id=shippingid)
                shipping.status = "Delivered"
                shipping.save()
            if action == "PENDING":
                shipping = ShippingInformation.objects.get(id=shippingid)
                shipping.status = "Pending"
                shipping.save()

            if action == "OUT_DELIVERY_ORDER":
                shipping = ShippingInformation.objects.get(id=shippingid)
                shipping.status = "Out for delivery"
                shipping.save()

    else:
        return redirect("login")