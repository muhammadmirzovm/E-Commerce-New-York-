from django.urls import path
from .views import CartDetailView, CartAddView, CartUpdateView, CartRemoveView

urlpatterns = [
   path("cart/", CartDetailView.as_view(), name="cart_detail"),
   path("cart/add/<int:product_id>/", CartAddView.as_view(), name="cart_add"),
   path("cart/update/<int:product_id>/", CartUpdateView.as_view(), name="cart_update"),
   path("cart/remove/<int:product_id>/", CartRemoveView.as_view(), name="cart_remove"),
]
