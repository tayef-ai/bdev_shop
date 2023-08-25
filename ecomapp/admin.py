from django.contrib import admin
from .models import Customer, Product, OrderPlaced, Cart, Category, Contact

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'shipping_address', 'phone']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'image']

@admin.register(OrderPlaced)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'order_date', 'status']

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'categoryname']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'cname', 'phone', 'email', 'message', 'date']