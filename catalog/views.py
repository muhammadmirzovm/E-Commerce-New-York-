from django.db.models import Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Product, Category
from .forms import ProductForm, RevievForm
from .mixins import SellerRequiredMixin, OwnerRequiredMixin, LoginRequiredMixin 
from django.urls import reverse_lazy
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.db.models import Q

class ProductListView(ListView):
   model = Product
   template_name = "catalog/product_list.html"
   context_object_name = "products"
   paginate_by = 12
   def get_queryset(self):
       qs = (Product.objects.filter(is_active=True).select_related("category", "seller")
           .order_by("-created_at"))
      
       q = self.request.GET.get("q", "").strip()
       if q:
           qs = qs.filter(
               Q(name__icontains=q) |
               Q(short_description__icontains=q) |
               Q(description__icontains=q))
       # 2) Category filter: category=slug
       cat_slug = self.request.GET.get("category", "").strip()
       if cat_slug:
           cat = Category.objects.filter(slug=cat_slug).first()
           
           if cat: #Mebellar -> Oshxona mebellari , Yotoqxona mebellari, Mehmonxona mebellari 
               child_ids = list(cat.children.values_list("id", flat=True))
               qs = qs.filter(category_id__in=[cat.id] + child_ids)
       # 3) Price range: min_price / max_price
       min_price = self.request.GET.get("min_price", "").strip()
       max_price = self.request.GET.get("max_price", "").strip()
       try:
           if min_price:
               qs = qs.filter(price__gte=Decimal(min_price))
           if max_price:
               qs = qs.filter(price__lte=Decimal(max_price))
       except InvalidOperation:
           messages.warning(self.request, "Narx maydoniga faqat son kiriting (masalan: 100 yoki 99.99) ⚠️")
       # 4) Sort: sort
       sort = self.request.GET.get("sort", "latest")
       if sort == "price_asc":
           qs = qs.order_by("price")
       elif sort == "price_desc":
           qs = qs.order_by("-price")
       else:
           qs = qs.order_by("-created_at")
       return qs
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Category dropdown uchun categorylar #Mebellar -> Mexmonxona 
       context["categories"] = Category.objects.filter(parent__isnull=True).order_by("name")
       # Hozirgi filter qiymatlarini template’ga qaytarish (input’larda saqlash uchun)
       context["q"] = self.request.GET.get("q", "").strip()
       context["category"] = self.request.GET.get("category", "").strip()
       context["min_price"] = self.request.GET.get("min_price", "").strip()
       context["max_price"] = self.request.GET.get("max_price", "").strip()
       context["sort"] = self.request.GET.get("sort", "latest")
       # Pagination bosilganda query yo‘qolmasin: page dan boshqa hammasini saqlaymiz
       params = self.request.GET.copy()
       params.pop("page", None)
       context["querystring"] = params.urlencode()
       return context

    
from django.db.models import Avg , Count  
class ProductDetailView(DetailView):
   model = Product
   template_name = "catalog/product_detail.html"
   context_object_name = "product"
   def get_context_data(self, **kwargs):
      ctx = super().get_context_data(**kwargs)
      product = self.object
      ctx["reviews"] = product.reviews.select_related("user").order_by("-created_at")
      ctx["avg_reting"] = product.reviews.aggregate(a=Avg("rating"))["a"] or 0
      ctx["reviews_count"] = product.reviews.aggregate(c=Count("id"))["c"]
      ctx["can_review"] = can_review(self.request.user , product)
      if self.request.user.is_authenticated:
          ctx["already_reviawed"] = product.reviews.filter(user=self.request.user).exists()
      else:
          ctx["already_reviawed"] = False
      return ctx
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




class ReviewCreatedView(LoginRequiredMixin , CreateView):
    model = Review
    form_class = RevievForm
    template_name = "catalog/review_form.html"
    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product , slug=kwargs["slug"] , is_active=True)
        
        if not can_review(request.user , self.product):
            messages.error(request , "Review yozish uchun avval sotib olib ,qabul qilishingiz kerak")
            return redirect("product_detail" , slug=self.product.slug)
        if Review.object.filter(product=self.product , user=request.user).exists():
            messages.info(request ,"Siz bu mahsulotga alaqachon review yozib bo'lgansiz")
            return redirect("product_detail" , slug=self.product.slug)
        return super().dispatch(request , *args ,**kwargs)


    def form_valid(self,form):
        review = form.save(commit = False)
        review_product = self.product
        review_user = self.request.user
        review.save()
        messages.success(self.request, "Review saqlandi")
        return redirect ("product_detail", slug = self.product.slug)
    
    
    
