from django.db import models
from django.contrib.auth.models import User

STATUS = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
)
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shipping_address = models.TextField(null=True)
    phone = models.CharField(max_length=100, null=True)

class Category(models.Model):
    categoryname = models.CharField(max_length=100)
    image = models.ImageField(default="product/store-4156934_1280.png", blank=True)
    def __str__(self):
        return self.categoryname
    

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    description = models.TextField()
    brand = models.CharField(max_length=100, null=True, blank=True, default='No Brand')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product')

    @property
    def price(self):
        if self.discounted_price is None:
            return self.selling_price
        else:
            return self.discounted_price

class Cart(models.Model):
    user = models.ForeignKey(User, related_name="user_cart", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        if self.product.discounted_price is None:
            return self.quantity * self.product.selling_price
        else:
            return self.quantity * self.product.discounted_price

class OrderPlaced(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now=True)
    status = models.CharField(default='Pending', choices=STATUS, max_length=100)

    @property
    def total_cost(self):
        if self.product.discounted_price is None:
            return self.quantity * self.product.selling_price
        else:
            return self.quantity * self.product.discounted_price
        
class Contact(models.Model):
    cname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)