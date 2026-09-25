from django.db import models
from django.conf import settings
from decimal import Decimal
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def subtotal(self):
        return sum((item.unit_price * item.qty) for item in self.items.all())

    def delivery(self):
        return Decimal("0.00") if self.subtotal() >= Decimal("500000000.00") else Decimal("25.00")

    def total(self):
        return self.subtotal() + self.delivery()

    def total_qty(self):
        return sum(item.qty for item in self.items.all())



from decimal import Decimal
from catalog.models import Product
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")

    qty = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.qty}"

    def line_total(self):
        return self.unit_price * self.qty
