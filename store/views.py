#/home/siisi/e-commerce/store/views.py

from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

from datetime import datetime, timezone


def category(request, foo):
    # Replace Hyphens with Spaces
    foo = foo.replace('-', ' ')
    # Grab the category from the url
    try:
        # Look up the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
        context = {
            'category' : category,
            'products' : products,
            'date' : date
        }
        return render(request, 'category.html', context)
    except:
        messages.warning(
            request, ("That Category Doesn't Exist, please try again.")
            )
        return redirect('home')

    date = datetime.now(timezone.utc).strftime("%a %d %B %Y")

    context = {
        'category' : category,
        'date' : date
    }
    return render(request, 'category.html', context)


def category_list(request):
    categories = Category.objects.all()
    date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
    
    context = {
        'categories': categories,
        'date': date
    }
    return render(request, 'category_list.html', context)


def product(request, pk):
    product = Product.objects.get(id=pk)
    date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
    
    context = {
        'product' : product,
        'date' : date
    }
    return render(request, 'product.html', context)


def home(request):
    products = Product.objects.all()
    date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
    
    context = {
        'products' : products,
        'date' : date
    }
    return render(request, 'home.html', context)


def about(request):
    date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
    
    context = {
        'date' : date
    }
    return render(request, 'about.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, (f"{user.username} Log In Successfully 👌🏿"))
            return redirect('home')
        else:
            messages.warning(request, ("There was an error, please try again. 😭"))
            return redirect('login')
    else:
        date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
        context = {
            'date' : date
        }
        return render(request, 'login.html', context)
        

def logout_user(request):
    username = request.user.username  # Get the name before logout
    logout(request)
    messages.success(request, f"Logout successful. Goodbye, {username} 😉!")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if  form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (f"{user.username} Successfully Registered 👌🏿"))
            return redirect('home')
        else:
            messages.warning(request, ("Whoops! There was a problem Registering, please try again 🤣."))
            return redirect('register')
    else:
        date = datetime.now(timezone.utc).strftime("%a %d %B %Y")

        context = {
            'form' : form,
            'date' : date
        }
        return render(request, 'register.html', context)
