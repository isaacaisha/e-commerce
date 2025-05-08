#/home/siisi/e-commerce/store/views.py

from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms

from datetime import datetime, timezone


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        info_form = UserInfoForm(request.POST or None, instance=current_user)

        if info_form.is_valid():
            info_form.save()

            #login(request, current_user)
            messages.success(request, (
                f"{request.user.username} Info Has Been Updated Successfully 👌🏿!"
                ))
            return redirect('update_info')
        date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
        context = {
            'info_form': info_form,
            'date' : date
        }
        return render(request, 'update_info.html', context)
    else:
        messages.warning(request, "You must Be Logged In To Access That Page 🤣.")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the password_form
        if request.method == 'POST':
            password_form = ChangePasswordForm(current_user, request.POST)
            # Is the password_form valid
            if password_form.is_valid():
                password_form.save()
                messages.success(request, (
                    f"{current_user.username}, Your Password Has Been Updated Successfully 👌🏿!"
                    ))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(password_form.errors.values()):
                    messages.warning(request, error)
                    return redirect('update_password')
        else:
            password_form = ChangePasswordForm(current_user)
            date = datetime.now(timezone.utc).strftime("%a %d %B %Y")

            context = {
                'password_form': password_form,
                'date' : date
            }
            return render(request, 'update_password.html', context)
    else:
        messages.warning(request, "You must Be Logged In To Access That Page 😭.")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, (
                f"{current_user.username} Has Been Updated Successfully 👌🏿!"
                ))
            return redirect('home')
        date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
        context = {
            'user_form': user_form,
            'date' : date
        }
        return render(request, 'update_user.html', context)
    else:
        messages.warning(request, "You must Be Logged In To Access That Page 🤣.")
        return redirect('home')


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
            messages.success(request, (f"Welcome {user.username}, You've Been Log In Successfully 👌🏿!"))
            return redirect('home')
        else:
            messages.warning(request, ("There was an error, please try again. 😭."))
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
    date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create Profile via signal
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, f"{user.username} Successfully Registered 👌🏿!")
            return redirect('update_info')
        else:
            # Form invalid: render with errors
            messages.warning(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    context = {
        'form': form,
        'date': date,
    }
    return render(request, 'register.html', context)
