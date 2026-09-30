from django import forms
from .models import Order, OrderItem

class CheckoutForm(forms.ModelForm):
   class Meta:
       model = Order
       fields = ("full_name", "phone", "address", "delivery_method", "note") 


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ("status",)
