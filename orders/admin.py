from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):# order ichida itemlarni jadval qilib ko‘rsatadi
   model = OrderItem
   extra = 1 # bo‘sh qator qo‘shmaydi
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display = ("id", "user","created_at")# admin listda ko‘rinadigan ustunlar
   list_filter = ("created_at",)  # filter
   inlines = [OrderItemInline]  # order sahifasida itemlar ham chiqadi
