from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Customer(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic =models.ImageField(null =True, blank= True, default='/download.png')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

   

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = [
        ('prime', 'prime'),
        ('new', 'new'),
    ]
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    price = models.FloatField(null=True)
    tag = models.ManyToManyField(Tag)
    image=models.CharField(max_length=2550,null=True)
   

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = [
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),

    ]
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    note = models.CharField(max_length=200, null=True,blank=True,default='general order')

    def __str__(self):
        return  self.product.name

