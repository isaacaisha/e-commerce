# /home/siisi/e-commerce/cart/cart.py

from store.models import Product, Profile

class Cart:
    def __init__(self, request):
        self.session = request.session

        # Get request
        self.request = request

        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def db_add(self, product, quantity):
        pid = str(product)
        qty = int(quantity)
        if pid in self.cart:
            self.cart[pid] = int(self.cart[pid]) + qty
        else:
            self.cart[pid] = qty
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single quote into doble quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        pid = str(product.id)
        qty = int(quantity)
        if pid in self.cart:
            self.cart[pid] = int(self.cart[pid]) + qty
        else:
            self.cart[pid] = qty
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single quote into doble quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        ## Convert string IDs to integers
        #product_ids = [int(pid) for pid in self.cart.keys()]
        product_ids = self.cart.keys()
        products = Product.objects.in_bulk(product_ids)
        return sum(
            (p.sale_price if p.is_sale else p.price) * qty 
            for pid, qty in self.cart.items() 
            if (p := products.get(int(pid)))
        )

    def __len__(self):
        # distinct product count
        return len(self.cart)

    @property
    def total_quantity(self):
        # total sum of all quantities
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

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single quote into doble quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def delete(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single quote into doble quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
