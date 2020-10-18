from django.shortcuts import render
from inventory.models import Item
from .models import Order, OrderItem
from django.views.generic import DetailView, ListView

# Create your views here.
def home(request):
    return render(request, 'home.html')

def view_404(request, *args, **kwargs):
    return render(request,'partial/404.html',{'title':'Oops! Page Not Found!!'}, status=404)

class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = "client_side/home.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "client_side/item_detail.html"

def cart(request):
    context = {}
    order = Order.objects.get_or_create(user=request.user, status='NO')[0]
    order_items = order.items.all()
    context['order'] = order
    context['order_items'] = order_items
    return render(request, 'client_side/cart.html', context)

