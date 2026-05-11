from .models import Order


def cart_total(request):
    total_quantity = 0
    if request.session.session_key:
        order = Order.objects.filter(session_key=request.session.session_key, is_completed=False).first()
        if order:
            total_quantity = sum(item.quantity for item in order.items.all())

    return {'cart_total_quantity': total_quantity}
from .models import Category

def categories_processor(request):
    return {'categories': Category.objects.all()}