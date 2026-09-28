from django.urls import path
from .views import CheckoutView, MyOrdersListView, OrderDetailView

urlpatterns = [
   path("checkout/", CheckoutView.as_view(), name="checkout"),  # checkout
   path("my-orders/", MyOrdersListView.as_view(), name="my_orders"),  # history
   path("my-orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),  # detail
]
