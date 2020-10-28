from .models import Category
from main.models import Order
from django.db.models import Count

def category(request):
    return {
        'categories': Category.objects.parents(),
        'cart_items': Order.objects.get_or_create(user=request.user, status='NO')[0].items.all().count() if request.user.is_authenticated else None,
        }