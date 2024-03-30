from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Customer(models.Model):

    user = models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)


    phone_field = models.CharField(max_length=12,blank=False)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=100)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE,null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    desc = models.TextField()
    price = models.FloatField(default=0.0)
    product_available_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products();


class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('300 TO 500','300 TO 500'),
        ('500 TO 700','500 TO 700'),
        ('700 TO 1000', '700 TO 1000'),
        ('1000 TO 1200', '1000 TO 1200'),
        ('1200 TO 1500', '1200 TO 1500'),
    )

    price = models.CharField(choices=FILTER_PRICE,max_length=60)

    def __str__(self):
        return self.price


class Shop(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    company_name = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return self.email


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    pincode = models.IntegerField()
    phone = models.IntegerField()
    address1 = models.TextField(max_length=100)
    address2 = models.TextField(max_length=100)
    city = models.CharField(max_length=100)
    amount = models.IntegerField()
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True)
    date = models.DateField(auto_now_add=True)



    def __str__(self):
        return self.Customer.user

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/Order_Img')
    quantity = models.CharField(max_length=20)
    price = models.FloatField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return self.Customer.user