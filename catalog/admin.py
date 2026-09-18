from django.contrib import admin
from .models import Category, Product, ProductImage
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ("name", "parent")
   search_fields = ("name",)
   prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
   model = ProductImage
   extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
   list_display = ("name", "seller", "price", "stock", "is_active", "created_at")
   list_filter = ("is_active", "category")
   search_fields = ("name", "short_description", "description")
   prepopulated_fields = {"slug": ("name",)}
   inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
   list_display = ("product", "alt_text")


