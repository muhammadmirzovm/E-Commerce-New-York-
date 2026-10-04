from orders.models import OrderItem
def can_review(user, product):
    if not user.is_authenticaticated:
        return False
    return OrderItem.objects.filter(
        order_user = user,
        product=product,
        status = "deliverid"
    ).exists()