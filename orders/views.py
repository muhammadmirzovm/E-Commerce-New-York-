from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from cart.utils import get_or_create_cart  # cartni olish uchun (sizda bor)
from .forms import CheckoutForm
from django.db import transaction
from django.shortcuts import redirect
from .models import Order , OrderItem



class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "orders/checkout.html" 
    form_class = CheckoutForm  
    success_url = reverse_lazy("my_orders") 
    def get_context_data(self, **kwargs):
       ctx = super().get_context_data(**kwargs)
       cart = get_or_create_cart(self.request.user)  # user cartini olamiz
       ctx["cart"] = cart  # template’da ko‘rsatish uchun
       ctx["items"] = cart.items
       ctx["subtotal"] = cart.subtotal()  # cart subtotal
       ctx["delivery"] = cart.delivery()  # cart delivery
       ctx["total"] = cart.total()  # cart total
       return ctx
    @transaction.atomic
    def form_valid(self, form):
       cart = get_or_create_cart(self.request.user)  # cartni olamiz
       if cart.items.count() == 0:  # cart bo‘sh bo‘lsa order qilmaymiz
           messages.error(self.request, "Savatcha bo‘sh ❌")
           return redirect("cart_detail")
       order = form.save(commit=False)  # hozircha DB ga saqlamaymiz
       order.user = self.request.user  # order egasi — hozirgi user
       order.save()  # endi DB ga saqlaymiz (order id hosil bo‘ladi)
       # Cart itemlardan OrderItem yasaymiz + stock kamaytiramiz
       for item in cart.items.all():
           product = item.product  # mahsulot obyekt
           if product.stock < item.qty:  # stock yetmasa
               messages.error(self.request, f"'{product.name}' uchun stock yetarli emas ❌")
               raise ValueError("Buncha mahsulot omborda yo'q")  # atomic sabab hammasi bekor bo‘ladi

           OrderItem.objects.create(
               order=order,  # qaysi order
               product=product,  # qaysi product
               seller=product.seller,  # buyurtma qaysi sotuvchiga tegishli
               qty=item.qty,  # miqdor
               unit_price=item.unit_price,  # cartdagi narx
           )

           product.stock -= item.qty
           product.save(update_fields=["stock"])  

       cart.items.all().delete()

       messages.success(self.request, f"Buyurtma yaratildi ✅ (Order #{order.id})")
       return redirect("order_detail", pk=order.pk)  


class MyOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/my_orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at") 

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # boshqa user orderini ocholmaydi





