from .models import Category
from main.models import Order
from django.db.models import Count

def category(request):
    return {
        'categories': Category.objects.parents(),
        'cart_items': Order.objects.get(user=request.user, status='NO').items.all().count(),
        }