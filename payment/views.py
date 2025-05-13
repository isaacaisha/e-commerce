# /home/siisi/e-commerce/payment/views.py

from django.shortcuts import render
from django.utils import timezone

from cart.cart import Cart

from payment.forms import ShippingForm
from payment.models import ShippingAddress


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


def payment_success(request):
    return render(request, 'payment/payment_success.html', {
        'date': _current_date(),
    })
