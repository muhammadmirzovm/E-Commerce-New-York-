from django.urls import path
from . import views

urlpatterns = [
   path("", views.ProductListView.as_view(), name="home"),
   path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
   path("seller/products/", views.SellerProductListView.as_view(), name="seller_products"),
   path("seller/products/add/", views.SellerProductCreateView.as_view(), name="seller_product_add"),
   path("seller/products/<int:pk>/edit/", views.SellerProductUpdateView.as_view(), name="seller_product_edit"),
   path("seller/products/<int:pk>/delete/", views.SellerProductDeleteView.as_view(), name="seller_product_delete"),

]


