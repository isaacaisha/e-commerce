# /home/siisi/e-commerce/store/views.py

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from cart.cart import Cart
from .models import Product, Category, Profile
from .forms import (
    SignUpForm,
    UpdateUserForm,
    ChangePasswordForm,
    UserInfoForm,
    ProductForm
)

from payment.models import ShippingAddress
from payment.forms import ShippingForm

def _current_date():
    return timezone.now().strftime("%a %d %B %Y")

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {
        'products': products,
        'date': _current_date(),
    })

def about(request):
    return render(request, 'about.html', {
        'date': _current_date(),
    })

@login_required
def create_product(request):
    if not request.user.is_superuser:
        messages.warning(request, "You must be a superuser to access this page.")
        return redirect('home') 

    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product created successfully.")
        return redirect('home')

    return render(request, 'create_product.html', {
        'form': form,
        'date': _current_date(),
    })

def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product.html', {
        'product': product,
        'date': _current_date(),
    })

def category(request, foo):
    name = foo.replace('-', ' ')
    category = get_object_or_404(Category, name=name)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'date': _current_date(),
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {
        'categories': categories,
        'date': _current_date(),
    })

def search(request):
    context = {'date': _current_date()}
    if request.method == 'POST':
        term = request.POST.get('searched', '').strip()
        if term:
            results = Product.objects.filter(
                Q(name__icontains=term) | Q(description__icontains=term)
            )
            if results.exists():
                context.update({'searched': results})
                return render(request, 'search.html', context)
        messages.warning(request, "No matching products found. Please try again.")
        return redirect('search')
    return render(request, 'search.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            current_user, _ = Profile.objects.get_or_create(user=request.user)
            saved_cart = current_user.old_cart
            if saved_cart:
                try:
                    converted_cart = json.loads(saved_cart)
                    cart = Cart(request)
                    for pid, quantity in converted_cart.items():
                        try:
                            product = Product.objects.get(id=int(pid))
                            cart.add(product=product, quantity=quantity)
                        except Product.DoesNotExist:
                            continue
                except json.JSONDecodeError:
                    messages.warning(request, "Your previous cart could not be restored due to format error.")
            messages.success(request, f"Welcome {user.username}, you are now logged in!")
            return redirect('home')
        messages.warning(request, "Invalid credentials. Please try again.")
        return redirect('login')
    return render(request, 'login.html', {'date': _current_date()})

def logout_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f"Goodbye, {username}!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, f"{user.username} registered successfully.")
            return redirect('update_info')
        messages.warning(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'register.html', {
        'form': form,
        'date': _current_date(),
    })

@login_required
def update_info(request):
    profile = get_object_or_404(Profile, user=request.user)
    shipping_user, _ = ShippingAddress.objects.get_or_create(user=request.user)

    form = UserInfoForm(request.POST or None, instance=profile)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

    if request.method == "POST" and form.is_valid() and shipping_form.is_valid():
        form.save()
        shipping_form.save()
        messages.success(request, f"{request.user.username}'s information updated successfully.")
        return redirect('update_info')

    return render(request, 'update_info.html', {
        'info_form': form,
        'shipping_form': shipping_form,
        'date': _current_date(),
    })

@login_required
def update_user(request):
    form = UpdateUserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        login(request, request.user)
        messages.success(request, f"{request.user.username} updated successfully.")
        return redirect('home')
    return render(request, 'update_user.html', {
        'user_form': form,
        'date': _current_date(),
    })

@login_required
def update_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            login(request, request.user)
            messages.success(request, "Password updated successfully.")
            return redirect('update_user')
        for err in form.errors.values():
            messages.warning(request, err)
        return redirect('update_password')
    form = ChangePasswordForm(request.user)
    return render(request, 'update_password.html', {
        'password_form': form,
        'date': _current_date(),
    })
