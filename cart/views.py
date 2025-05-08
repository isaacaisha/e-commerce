# /home/siisi/e-commerce/cart/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timezone

from .cart import Cart
from store.models import Product

def cart_summary(request):
    cart = Cart(request)
    context = {
        'cart_products': cart.get_prods(),
        'quantities': cart.get_quants(),
        'total_quantity': cart.total_quantity,
        'totals' : cart.cart_total(),
        'date': datetime.now(timezone.utc).strftime("%a %d %B %Y"),
    }
    return render(request, 'cart_summary.html', context)

def cart_add(request):
    if request.POST.get('action') == 'post':
        pid = int(request.POST['product_id'])
        qty = int(request.POST['product_qty'])
        product = get_object_or_404(Product, id=pid)

        cart = Cart(request)
        cart.add(product, qty)

        msg = f"Added {product.name} (x{qty}) to your cart."
        return JsonResponse({
            'status': 'success',
            'distinct_count': len(cart),
            'total_quantity': cart.total_quantity,
            'message': msg,
        })

def cart_update(request):
    if request.POST.get('action') == 'post':
        pid = int(request.POST['product_id'])
        qty = int(request.POST['product_qty'])
        product = get_object_or_404(Product, id=pid)

        cart = Cart(request)
        cart.update(pid, qty)

        msg = f"Updated '{product.name}' quantity to {qty}."
        return JsonResponse({
            'status': 'updated',
            'distinct_count': len(cart),
            'total_quantity': f'Total: {cart.total_quantity}',
            'cart_total': cart.cart_total(),
            'message': msg,
        })

def cart_delete(request):
    if request.POST.get('action') == 'post':
        pid = int(request.POST['product_id'])
        cart = Cart(request)
        cart.delete(pid)
        product = get_object_or_404(Product, id=pid)

        msg = f"Removed '{product.name}' from your cart."
        return JsonResponse({
            'status': 'deleted',
            'distinct_count': len(cart),
            'total_quantity': cart.total_quantity,
            'cart_total': cart.cart_total(),
            'message': msg,
        })
