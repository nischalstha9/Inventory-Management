from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView
from .forms import ItemCreationForm, DebitTransactionForm, CreditTransactionForm, DebitPaymentForm
from .models import Item, DebitTransaction, Category, CreditTransaction, Payment
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from django.core.exceptions import ValidationError

def allowed_users(allowed_types=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user._type in allowed_types[0]:
                    return view_func(request, *args, **kwargs)
            else:
                return redirect('/')
        return wrapper_func
    return decorator

# Create your views here.
def index(request):
    return render(request, "inventory/item_list.html")

class ItemCreationVIew(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ItemCreationForm
    template_name = 'inventory/item_creation.html'
    success_url = "../"

    def test_func(self):
        return self.request.user._type == 'ADMIN'

class ItemListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Item
    template_name = "inventory/item_list.html"
    context_object_name = 'items'
    paginate_by = 50

    def test_func(self):
        return self.request.user._type == 'ADMIN'

class ItemUpdateVIew(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ItemCreationForm
    template_name = 'inventory/item_creation.html'
    success_url = "../../"
    queryset = Item.objects.all()

    def test_func(self):
        return self.request.user._type == 'ADMIN'

@allowed_users(allowed_types = ['ADMIN'])
def add_to_inventory(request):
    context = {'header' : 'Add Stock'}
    form = DebitTransactionForm(request.POST or None)
    context['form']= form
    if request.method == 'POST':
        print(request.POST)
        item = request.POST.get('item')
        cp = int(request.POST.get('cost'))
        sp = int(request.POST.get('selling_price'))
        qty = int(request.POST.get('quantity'))
        paid = int(request.POST.get('paid'))
        item = Item.objects.get(id=item)
        item.cost_price = cp
        item.quantity = item.quantity+qty
        if sp < cp:
            messages.warning(request, 'Selling Price cannot be less than Cost Price.')
            return render(request, "inventory/add_stock.html", context)            
        else:
            item.selling_price = sp
        item.save()
        trans = form.save(request.POST)
        payment = Payment.objects.create(transaction = trans, amount=paid)
        payment.save()
        return redirect("inventory:items-list")
    return render(request, "inventory/add_stock.html", context)

class DebitTransactionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DebitTransaction
    template_name = "inventory/dr_transactions.html"
    context_object_name = 'transactions'
    paginate_by=50
    def test_func(self):
        return self.request.user._type == 'ADMIN'

class DebitTransactionUpdateView(UpdateView):
    model = DebitTransaction
    fields = ['remarks']
    template_name = "inventory/add_stock.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Update Transaction Info'
        return context
    
    def get_success_url(self):
        return reverse('inventory:debit-transactions')

@allowed_users(allowed_types = ['ADMIN'])
def sell_from_inventory(request):
    context = {'header' : 'Sell Stock'}
    form = CreditTransactionForm(request.POST or None)
    context['form']= form
    if request.method == 'POST':
        print(request.POST)
        item = request.POST.get('item')
        qty = int(request.POST.get('quantity'))
        paid = int(request.POST.get('paid'))
        item = Item.objects.get(id=item)
        item.quantity = item.quantity-qty
        item.save()
        form.instance._type = 'STOCK OUT'
        trans = form.save()
        Payment.objects.create(transaction = trans, amount = paid)
        return redirect("inventory:items-list")
    return render(request, "inventory/add_stock.html", context)

class CreditTransactionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CreditTransaction
    template_name = "inventory/cr_transactions.html"
    context_object_name = 'transactions'
    paginate_by=50
    def test_func(self):
        return self.request.user._type == 'ADMIN'

class CreditTransactionUpdateView(UpdateView):
    model = CreditTransaction
    fields = ['remarks']
    template_name = "inventory/add_stock.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Update Transaction Info'
        return context
    
    def get_success_url(self):
        return reverse('inventory:credit-transactions')
    
def DebitTransactionPaymentCreateView(request):
    form = DebitPaymentForm
    context = {}
    context['form'] = form
    context['header'] = "Add Payment for Stock In"
    if request.method=="POST":
        trans = request.POST.get('transaction')
        amt = int(request.POST.get('amount'))
        trans = DebitTransaction.objects.get(id=trans)
        trans.paid = trans.paid + amt
        trans.save()
        Payment.objects.create(transaction = trans, amount = amt)
        # return reverse("inventory:debit-transactions")
    return render(request, "inventory/add_stock.html", context)




    