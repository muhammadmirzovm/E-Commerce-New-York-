from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Product
from .forms import ProductForm
from .mixins import SellerRequiredMixin, OwnerRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
       return (
           Product.objects.filter(is_active=True).select_related\
               ("category", "seller").order_by("-created_at")
       )
    
class ProductDetailView(DetailView):
   model = Product
   template_name = "catalog/product_detail.html"
   context_object_name = "product"



class SellerProductListView(SellerRequiredMixin, ListView):
    model = Product
    template_name = "catalog/seller/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by("-created_at")
class SellerProductCreateView(SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/seller/product_form.html"
    success_url = reverse_lazy("seller_products")
    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, "Mahsulot qo‘shildi ✅")
        return super().form_valid(form)

class SellerProductUpdateView(SellerRequiredMixin, OwnerRequiredMixin, UpdateView):
   model = Product
   form_class = ProductForm
   template_name = "catalog/seller/product_form.html"
   success_url = reverse_lazy("seller_products")

   def form_valid(self, form):
       messages.success(self.request, "Mahsulot yangilandi ✅")
       return super().form_valid(form)
class SellerProductDeleteView(SellerRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/seller/product_confirm_delete.html"
    success_url = reverse_lazy("seller_products")
    def form_valid(self, form):
        messages.success(self.request, "Mahsulot o‘chirildi ✅")
        return super().form_valid(form)


