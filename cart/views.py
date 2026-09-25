from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from catalog.models import Product
from .models import CartItem
from .utils import get_or_create_cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart_detail.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs) 
        cart = get_or_create_cart(self.request.user)
        ctx["cart"] = cart
        ctx["items"] = cart.items
        ctx["subtotal"] = cart.subtotal()
        ctx["delivery"] = cart.delivery()
        ctx["total"] = cart.total()
        return ctx
class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = get_or_create_cart(request.user)
        product = get_object_or_404(Product, id=product_id, is_active=True)
        qty = int(request.POST.get("qty", 1))
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"qty": qty, "unit_price": product.price},
        )
        if not created:
            item.qty += qty
            item.unit_price = product.price  
            item.save()
        messages.success(request, "Savatchaga qo‘shildi ✅")
        return redirect("cart_detail")
class CartUpdateView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        qty = int(request.POST.get("qty", 1))
        if qty <= 0:
            item.delete()
            messages.warning(request, "Item o‘chirildi 🗑️")
        else:
            item.qty += 1
            item.save()
            messages.info(request, "Miqdor yangilandi ✅")
        return redirect("cart_detail")
class CartRemoveView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.delete()
        messages.warning(request, "Savatchadan o‘chirildi 🗑️")
        return redirect("cart_detail")

