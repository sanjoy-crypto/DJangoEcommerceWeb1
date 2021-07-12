from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from product.models import *
from home.models import *
from order.models import *
from home.template_context import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import *

# Create your views here.


@login_required(login_url='/login')
def index(request):

    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'profile': profile}
    return render(request, 'Home/user_profile.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url

            return redirect('/')
        else:
            messages.warning(
                request, "Login Error !! Username or Password is incorrect")
            return redirect('/login')

    context = {}
    return render(request, 'Home/login_page.html', context)


def logout_page(request):
    logout(request)
    return redirect('/login')


def signup_page(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/mavatar.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return redirect('/')
        else:
            messages.warning(request, form.errors)
            return redirect('/signup')

    context = {'form': form}
    return render(request, 'Home/signup_page.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'Home/user_update.html', context)


@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('/user')
        else:
            messages.error(
                request, 'Please correct the error below.<br>' + str(form.errors))
            return redirect('/user/password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'Home/user_password.html', {'form': form})


@login_required(login_url='/login')
def user_orders(request):

    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {'orders': orders}
    return render(request, 'Home/user_orders.html', context)


@login_required(login_url='/login')
def user_orderdetail(request, id):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'Home/user_order_detail.html', context)


@login_required(login_url='/login')
def user_order_product(request):

    current_user = request.user
    order_product = OrderProduct.objects.filter(
        user_id=current_user.id).order_by('-id')
    context = {'order_product': order_product}
    return render(request, 'Home/user_order_products.html', context)


@login_required(login_url='/login')
def user_order_product_detail(request, id, oid):

    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'Home/user_order_detail.html', context)


def user_comments(request):
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'comments': comments,
    }
    return render(request, 'Home/user_comments.html', context)

@login_required(login_url='/login')
def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return redirect('/user/comments')