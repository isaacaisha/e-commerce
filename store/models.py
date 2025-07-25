# /home/siisi/e-commerce/store/models.py

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=19, blank=True)
    address1 = models.CharField(max_length=199, blank=True)
    address2 = models.CharField(max_length=199, blank=True)
    city = models.CharField(max_length=199, blank=True)
    state = models.CharField(max_length=199, blank=True)
    zipcode = models.CharField(max_length=199, blank=True)
    country = models.CharField(max_length=199, blank=True)
    old_cart = models.CharField(max_length=199, blank=True, null=True)

    def __str__(self):
        return self.user.username

# create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# automate the profile thing
post_save.connect(create_profile, sender=User)


# Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


# Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=91)
    password = models.CharField(max_length=91)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# All of our Products
class Product(models.Model):
    name = models.CharField(max_length=91)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(default='', blank=True, null=True, max_length=250)
    image = models.ImageField(upload_to='uploads/products/')
    # Add Sale
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    def __str__(self):
        return self.name


# Customer Orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    adsress = models.CharField(default='', blank=True, max_length=91)
    phone = models.CharField(default='', blank=True, max_length=19)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
