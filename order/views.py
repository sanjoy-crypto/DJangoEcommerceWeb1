from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from home.models import *
from product.models import *
from user.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.template_context import *
from django.utils.crypto import get_random_string
# Create your views here.


def index(request):
    return HttpResponse('<h1> Order Page </h1>')


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    checkproduct = ShopCart.objects.filter(product_id=id)

    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return redirect(url)

    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to Shopcart")
        return redirect(url)


def shopcart(request):

    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_items = sum([item.quantity for item in shopcart])
    total = sum([item.product.price * item.quantity for item in shopcart])

    context = {'total': total, 'category': category,
               'shopcart': shopcart, 'setting': setting, 'total_items': total_items}
    return render(request, 'Home/shopcart_products.html', context)


@login_required(login_url='/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return redirect("/shopcart")


def orderproduct(request):

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = sum([item.product.price * item.quantity for item in shopcart])

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random code
            data.code = ordercode
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity

                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            # Clear & Delete shopcart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(
                request, "Your Order has been completed. Thank you ")
            return render(request, 'Home/Order_Completed.html', {'ordercode': ordercode})
        else:
            messages.warning(request, form.errors)
            return redirect("/order/orderproduct")

    form = OrderForm()

    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'form': form,
               'profile': profile
               }
    return render(request, 'Home/checkout.html', context)
