# /home/siisi/e-commerce/payment/views.py

import json
import stripe
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from paypal.standard.forms import PayPalPaymentsForm

from store.models import Product, Profile
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem


stripe.api_key = settings.STRIPE_SECRET_KEY


def _current_date():
    return timezone.now().strftime("%a %d %B %Y")


def _create_order(cart, user, shipping_info, invoice):
    # Prevent duplicate orders for the same invoice
    if Order.objects.filter(invoice=invoice).exists():
        return Order.objects.get(invoice=invoice)

    full_name = shipping_info.get('shipping_full_name', '').strip()
    email = shipping_info.get('shipping_email', '').strip()
    shipping_address = "\n".join([
        shipping_info.get('shipping_address1', ''),
        shipping_info.get('shipping_address2', ''),
        shipping_info.get('shipping_city', ''),
        shipping_info.get('shipping_state', ''),
        shipping_info.get('shipping_zipcode', ''),
        shipping_info.get('shipping_country', ''),
    ]).strip()

    order = Order.objects.create(
        user=user if user.is_authenticated else None,
        full_name=full_name,
        email=email,
        shipping_address=shipping_address,
        amount_paid=cart.cart_total(),
        invoice=invoice
    )

    for product in cart.get_prods():
        quantity = cart.get_quants().get(str(product.id), 0)
        if quantity > 0:
            price = product.sale_price if product.is_sale else product.price
            OrderItem.objects.create(
                order=order,
                user=user if user.is_authenticated else None,
                product=product,
                quantity=quantity,
                price=price
            )
    return order


def checkout(request):
    cart = Cart(request)
    shipping_user = None
    shipping_form = ShippingForm(request.POST or None)
    if request.user.is_authenticated:
        shipping_user, _ = ShippingAddress.objects.get_or_create(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

    context = {
        'cart_products': cart.get_prods(),
        'quantities': cart.get_quants(),
        'total_quantity': cart.total_quantity,
        'totals': cart.cart_total(),
        'shipping_user': shipping_user,
        'shipping_form': shipping_form,
        'date': _current_date(),
    }
    return render(request, 'payment/checkout.html', context)


def billing_info(request):
    if request.method != 'POST':
        messages.warning(request, "Access Denied.")
        return redirect('home')

    cart = Cart(request)
    shipping_data = request.POST.dict()
    request.session['my_shipping'] = shipping_data

    # Use existing invoice from session if available, else create new
    invoice = request.session.get('order_invoice')
    if not invoice:
        invoice = str(uuid.uuid4())
        request.session['order_invoice'] = invoice

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": cart.cart_total(),
        "item_name": "Shopping Cart Checkout",
        "no_shipping": "2",
        "invoice": invoice,
        "currency_code": "EUR",
        "notify_url": f"https://{request.get_host()}{reverse('paypal-ipn')}",
        "return_url": f"https://{request.get_host()}{reverse('payment_success')}",
        "cancel_return": f"https://{request.get_host()}{reverse('payment_failed')}",
    }
    paypal_form = PayPalPaymentsForm(initial=paypal_dict)

    # Create order only if not already created
    _create_order(cart, request.user, shipping_data, invoice)

    if request.user.is_authenticated:
        Profile.objects.filter(user=request.user).update(old_cart="")

    context = {
        'cart_products': cart.get_prods(),
        'quantities': cart.get_quants(),
        'total_quantity': cart.total_quantity,
        'totals': cart.cart_total(),
        'shipping_info': shipping_data,
        'billing_form': PaymentForm(),
        'my_shipping': shipping_data,
        'paypal_form': paypal_form,
        'date': _current_date(),
    }
    return render(request, 'payment/billing_info.html', context)


def process_order(request):
    if request.method != 'POST':
        messages.warning(request, "Access Denied.")
        return redirect('home')

    cart = Cart(request)
    shipping_data = request.session.get('my_shipping', {})
    invoice = request.session.get('order_invoice')

    if not invoice:
        # fallback: generate a new invoice and create order (rare case)
        invoice = str(uuid.uuid4())
        request.session['order_invoice'] = invoice

    # Only create order if it doesn't exist (usually it does)
    _create_order(cart, request.user, shipping_data, invoice)

    # Clear session cart, invoice and profile old cart
    request.session.pop('cart', None)
    request.session.pop('order_invoice', None)
    request.session.pop('my_shipping', None)

    if request.user.is_authenticated:
        Profile.objects.filter(user=request.user).update(old_cart="")

    messages.success(request, "Successfully Charged.")
    return redirect('home')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def shipped_dash(request):
    orders = Order.objects.filter(shipped=True)
    if request.method == 'POST':
        order = get_object_or_404(Order, id=request.POST.get('num'))
        order.shipped = False
        order.save()
        messages.success(request, "Shipping Status Updated!")
        return redirect('home')
    return render(request, 'payment/shipped_dash.html', {'orders': orders, 'date': _current_date()})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def not_shipped_dash(request):
    orders = Order.objects.filter(shipped=False)
    if request.method == 'POST':
        order = get_object_or_404(Order, id=request.POST.get('num'))
        order.shipped = True
        order.date_shipped = timezone.now()
        order.save()
        messages.success(request, "Shipping Status Updated!")
        return redirect('home')
    return render(request, 'payment/not_shipped_dash.html', {'orders': orders, 'date': _current_date()})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def orders(request, pk):
    order = get_object_or_404(Order, id=pk)
    items = OrderItem.objects.filter(order=pk)
    if request.method == 'POST':
        status = request.POST.get('shipping_status') == 'true'
        order.shipped = status
        if status:
            order.date_shipped = timezone.now()
        order.save()
        messages.success(request, "Shipping Status Updated!")
        return redirect('home')
    return render(request, 'payment/orders.html', {'order': order, 'items': items, 'date': _current_date()})


@login_required
def stripe_checkout(request):
    if request.method != 'POST':
        messages.warning(request, "Access Denied.")
        return redirect('home')

    cart = Cart(request)
    total_cents = int(cart.cart_total() * 100)

    shipping_data = request.POST.dict()
    request.session['my_shipping'] = shipping_data

    # Use existing invoice from session or create a new one
    invoice = request.session.get('order_invoice')
    if not invoice:
        invoice = str(uuid.uuid4())
        request.session['order_invoice'] = invoice

    request.session['stripe_invoice'] = invoice

    # Create unpaid order only if it doesn't exist
    _create_order(cart, request.user, shipping_data, invoice)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': 'Shopping Cart Checkout'},
                'unit_amount': total_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('payment_failed')),
        metadata={
            'user_id': request.user.id,
            'invoice': invoice,
        }
    )

    return redirect(session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except Exception as e:
        print(f"[Stripe Webhook] signature failure: {e}")
        return HttpResponse(status=400)

    if event['type'] != 'checkout.session.completed':
        return HttpResponse(status=200)

    session = event['data']['object']
    invoice = session.get('metadata', {}).get('invoice')

    if not invoice:
        print("[Stripe Webhook] no invoice metadata, skipping")
        return HttpResponse(status=200)

    try:
        order = Order.objects.get(invoice=invoice)
    except Order.DoesNotExist:
        print(f"[Stripe Webhook] no Order for invoice {invoice}")
        return HttpResponse(status=200)

    if not order.paid:
        order.paid = True
        order.save()
        print(f"[Stripe Webhook] Order {order.id} marked paid")

    return HttpResponse(status=200)


def payment_success(request):
    # Clear session after successful payment
    request.session.pop('cart', None)
    request.session.pop('order_invoice', None)
    request.session.pop('my_shipping', None)
    return render(request, 'payment/payment_success.html', {'date': _current_date()})


def payment_failed(request):
    return render(request, 'payment/payment_failed.html', {'date': _current_date()})
