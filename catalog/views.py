from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from .models import Product

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



    
