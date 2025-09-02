# /home/siisi/e-commerce/cart/cart.py

import json

from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def _persist_cart(self):
        if self.request.user.is_authenticated:
            Profile.objects.filter(user=self.request.user).update(old_cart=json.dumps(self.cart))

    def add(self, product, quantity):
        pid = str(product.id)
        qty = int(quantity)
        if pid in self.cart:
            self.cart[pid] += qty
        else:
            self.cart[pid] = qty
        self.session.modified = True
        self._persist_cart()

    def cart_total(self):
        product_ids = list(map(int, self.cart.keys()))
        products = Product.objects.in_bulk(product_ids)
        return sum(
            (p.sale_price if p.is_sale else p.price) * qty 
            for pid, qty in self.cart.items() 
            if (p := products.get(int(pid)))
        )

    def __len__(self):
        return len(self.cart)

    @property
    def total_quantity(self):
        return sum(self.cart.values())

    def get_prods(self):
        return Product.objects.filter(id__in=self.cart.keys())

    def get_quants(self):
        return self.cart

    def update(self, product_id, quantity):
        pid = str(product_id)
        qty = int(quantity)
        if pid in self.cart:
            self.cart[pid] = qty
            self.session.modified = True
            self._persist_cart()

    def delete(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.session.modified = True
            self._persist_cart()
