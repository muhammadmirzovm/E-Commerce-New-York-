from django.db import models
from django.conf import settings
from catalog.models import Product
from decimal import Decimal
class Order(models.Model):
    user = models.ForeignKey(  
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    full_name = models.CharField(max_length=120)  
    phone = models.CharField(max_length=30)  
    address = models.TextField()  
    delivery_method = models.CharField(max_length=50, default="standard")  
    note = models.TextField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f"#{self.id} Buyurtma  {self.user.username} tomonidan"  
class OrderItem(models.Model):
    STATUS_NEW = "new"  # yangi buyurtma
    STATUS_PROCESSING = "processing"  # tayyorlanmoqda
    STATUS_DELIVERED = "delivered"  # yetkazildi
    STATUS_CANCELED = "canceled"  # bekor qilindi
    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELED, "Canceled"),
    ]
    order = models.ForeignKey( 
        Order, on_delete=models.CASCADE, related_name="items")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)  # order holati
    product = models.ForeignKey(Product,
       on_delete=models.PROTECT,  # order bo‘lsa product o‘chib ketmasin (tarix saqlansin)
       related_name="order_items")
    seller = models.ForeignKey(  # buyurtma qaysi sotuvchiga borishini ajratish uchun
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sold_items")
    qty = models.PositiveIntegerField(default=1)  # soni
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))  # bitta narx
    def line_total(self):
       return self.unit_price * self.qty  
