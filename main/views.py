from django.shortcuts import render
from inventory.models import Item, Category
from .models import Order, OrderItem, CheckoutData
from django.views.generic import DetailView, ListView, CreateView
from django.utils import timezone
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def home(request):
    context = {}
    return render(request, 'home.html', context)

def view_404(request, *args, **kwargs):
    return render(request,'partial/404.html',{'title':'Oops! Page Not Found!!'}, status=404)

class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = "client_side/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'For You'
        return context
    

class ItemDetailView(DetailView):
    model = Item
    template_name = "client_side/item_detail.html"

@login_required
def cart(request):
    context = {}
    order = Order.objects.get_or_create(user=request.user, status='NO')[0]
    order_items = order.items.all()
    context['order'] = order
    context['order_items'] = order_items
    return render(request, 'client_side/cart.html', context)

class CheckoutDataCreateView(LoginRequiredMixin, CreateView):
    model = CheckoutData
    fields = ['contact', 'message', 'remarks']
    template_name = "client_side/checkout.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(user = self.request.user, status='NO')
        context["order"] = order
        return context
    def form_valid(self, form):
        if form.is_valid():
            order = Order.objects.get(user = self.request.user, status='NO')
            form.instance.order = order
            order.status = 'O'
            order.ordered_date = timezone.now()
            order.save()
            for i in order.items.all():
                i.ordered = True
                i.save()
            form.save()
        messages.success(self.request, "Your Order has been placed!")
        return redirect(reverse('main:cart'))


class MyOrderListView(LoginRequiredMixin ,ListView):
    model = Order
    context_object_name = 'orders'
    template_name = "client_side/my_orders.html"
    paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user = self.request.user).exclude(status='NO')
        return qs

class CategoryItemListView(ListView):
    model = Item
    template_name = "client_side/home.html"
    context_object_name = 'items'
    def get_queryset(self):
        qs = super().get_queryset()
        category = Category.objects.get(pk = self.kwargs.get('pk'))
        qs = qs.filter(category=category)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = Category.objects.get(pk = self.kwargs.get('pk'))
        return context
    
    

    

    

