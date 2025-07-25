# /home/siisi/e-commerce/cart/context_processor.py

from .cart import Cart


# Create context processor so our Cart can work on all pages of site
def cart(request):
    # Return the default data from our Cart
    c = Cart(request)
    return {
      'cart': c,
      'cart_total_quantity': sum(c.cart.values()),
    }
    