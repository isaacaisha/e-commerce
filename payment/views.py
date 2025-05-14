# /home/siisi/e-commerce/payment/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone

from cart.cart import Cart

from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem


def _current_date():
    return timezone.now().strftime("%a %d %B %Y")


def checkout(request):
    cart = Cart(request)

    if request.user.is_authenticated:
        # Checkout as logged in user
        # Get or create the user's ShippingAddress (assuming there's one per user)
        shipping_user = ShippingAddress.objects.filter(user=request.user).first()
        if not shipping_user:
            shipping_user = ShippingAddress(user=request.user)
        
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        context = {
            'cart_products': cart.get_prods(),
            'quantities': cart.get_quants(),
            'total_quantity': cart.total_quantity,
            'totals' : cart.cart_total(),
            'shipping_user' : shipping_user,
            'shipping_form' : shipping_form,
            'date': _current_date(),
        }
        return render(request, 'payment/checkout.html', context)
    else:
        # Checkout as Guest
        shipping_form = ShippingForm(request.POST or None)
        context = {
            'cart_products': cart.get_prods(),
            'quantities': cart.get_quants(),
            'total_quantity': cart.total_quantity,
            'totals' : cart.cart_total(),
            'shipping_form' : shipping_form,
            'date': _current_date(),
        }
        return render(request, 'payment/checkout.html', context)


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        context = {
            'cart_products': cart.get_prods(),
            'quantities': cart.get_quants(),
            'total_quantity': cart.total_quantity,
            'totals': cart.cart_total(),
            'shipping_info' : request.POST,
            'billing_form' : PaymentForm(),
            'my_shipping' :my_shipping,
            'date': _current_date(),
        }

        # Check if user is logged in
        if request.user.is_authenticated:
            return render(request, 'payment/billing_info.html', context)
        else:
            # Not logged in
            return render(request, 'payment/billing_info.html', context)
    else:
        messages.warning(request, "Access Denied.")
        return redirect('home')


def payment_success(request):
    return render(request, 'payment/payment_success.html', {
        'date': _current_date(),
    })


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(
                user=user, full_name=full_name, email=email,
                shipping_address=shipping_address, amount_paid=amount_paid
                )
            create_order.save()

            messages.success(request, "Successfuly Charged.")
            return redirect('home')

        else:
            # Not looged in
            # Create Order
            create_order = Order(
                full_name=full_name, email=email,
                shipping_address=shipping_address, amount_paid=amount_paid
                )
            create_order.save()
            
            messages.success(request, "Successfuly Charged.")
            return redirect('home')
    else:
        messages.warning(request, "Access Denied.")
        return redirect('home')


def payment_success(request):
    return render(request, 'payment/payment_success.html', {
        'date': _current_date(),
    })
