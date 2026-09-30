from django.urls import path
from . import views

urlpatterns = [
   path("checkout/", views.CheckoutView.as_view(), name="checkout"),  # checkout
   path("my-orders/", views.MyOrdersListView.as_view(), name="my_orders"),  # history
   path("my-orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),  # detail
   path("seller/orders/<int:pk>/status/", views.SellerOrderStatusUpdateView.as_view(), name="seller_order_status"),
   path("seller/orders/", views.SellerOrderItemListView.as_view(), name="seller_order_items"),
   path("seller/orders/item/<int:pk>/", views.SellerOrderItemDetailView.as_view(), name="seller_order_item_detail"),

]
