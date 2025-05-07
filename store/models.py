# /home/siisi/e-commerce/store/models.py

from django.db import models
import datetime


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
