from order.models import ShopCart
from django.contrib.auth.models import User
from home.models import *
from product.models import *


def get_filters(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_items = sum([item.quantity for item in shopcart])
    total = sum([item.product.price * item.quantity for item in shopcart])

    setting = Setting.objects.get(id=1)
    category = Category.objects.all()

    return {
        'total_items': total_items,
        'total': total, 'setting': setting, 'category': category
    }
