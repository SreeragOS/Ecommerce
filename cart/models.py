from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
# Create your models here.
class Cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    date_added = models.DateTimeField(auto_now_add=True)
    def subtotal(self):
        return self.product.price * self.quantity
    def __str__(self):
        return self.user.username
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    order_id = models.CharField(max_length=100, unique=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=50, default='Pending')
    payment_method = models.CharField(max_length=50)
    def __str__(self):
        return self.user.username
class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)