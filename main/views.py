from django.shortcuts import render
from inventory.models import Item
from .models import Order, OrderItem, CheckoutData
from django.views.generic import DetailView, ListView, CreateView
from django.utils import timezone
from django.shortcuts import redirect, reverse

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

class CheckoutDataCreateView(CreateView):
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
        return redirect(reverse('main:ordering_success'))
        # return super().form_valid(form)

def ordering_success(request):
    return render(request, 'client_side/ordering_success.html')
    

