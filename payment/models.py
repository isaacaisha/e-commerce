# /home/siisi/e-commerce/payment/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from store.models import Product


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=199)
    shipping_email = models.CharField(max_length=199)
    shipping_address1 = models.CharField(max_length=199)
    shipping_address2 = models.CharField(max_length=199, null=True, blank=True)
    shipping_city = models.CharField(max_length=199)
    shipping_state = models.CharField(max_length=199, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=199, null=True, blank=True)
    shipping_country = models.CharField(max_length=199)

    # Don't pluralize address
    class Meta:
        verbose_name_plural = "Shipping Addresss"

    def __str__(self):
        return f"Shipping Address - {str(self.id)}"

# create a user Shipping Address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

# automate the profile thing
post_save.connect(create_shipping, sender=User)


# Create Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=199)
    email = models.CharField(max_length=199)
    shipping_address = models.TextField(max_length=19999)
    amount_paid = models.DecimalField(max_digits=9, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order - {str(self.id)}"


# Create Order Items Model
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"Order Item - {str(self.id)}"
