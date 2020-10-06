from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import ItemCreationForm, DebitTransactionForm, CreditTransactionForm, DebitPaymentForm, CreditPaymentForm
from .models import Item, DebitTransaction, Category, CreditTransaction, Payment, Transaction
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from django_filters.views import FilterView
from .filters import DebitTransactionFilter
from datetime import datetime
from django.utils.timezone import make_aware
from django_summernote.widgets import SummernoteWidget

#custom decorator for filtering permission
def allowed_users(allowed_types=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user._type in allowed_types:
                    return view_func(request, *args, **kwargs)
            else:
                return redirect('/')
        return wrapper_func
    return decorator

# Create your views here.
def index(request):
    return render(request, "inventory/item_list.html")

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = "__all__"
    template_name = "inventory/big-form.html"
    success_url = "/"
    def test_func(self):
        return self.request.user._type == 'ADMIN'

class ItemCreationVIew(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ItemCreationForm
    template_name = 'inventory/big-form.html'
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
    template_name = 'inventory/big-form.html'
    success_url = "../../"
    queryset = Item.objects.all()

    def test_func(self):
        return self.request.user._type == 'ADMIN'

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = "inventory/delete_item.html"
    def get_success_url(self):
        return reverse('inventory:items-list')
    def test_func(self):
        return self.request.user._type == 'ADMIN'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


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
        if qty <= 0:
            messages.warning(request, 'Quantity must be greater than 0.')
            return render(request, "inventory/small-form.html", context)            
        paid = int(request.POST.get('paid'))
        item = Item.objects.get(id=item)
        item.cost_price = cp
        item.quantity = item.quantity+qty
        if sp < cp:
            messages.warning(request, 'Selling Price cannot be less than Cost Price.')
            return render(request, "inventory/small-form.html", context)            
        else:
            item.selling_price = sp
        item.save()
        trans = form.save(request.POST)
        payment = Payment.objects.create(transaction = trans, amount=paid)
        payment.save()
        return redirect("inventory:items-list")
    return render(request, "inventory/small-form.html", context)

def TransactionListView(request):
    return render(request, 'inventory/transactions.html')

class DebitTransactionListView(LoginRequiredMixin, UserPassesTestMixin, FilterView):
    model = DebitTransaction
    template_name = "inventory/dr_transactions.html"
    context_object_name = 'transactions'
    paginate_by=50
    def test_func(self):
        return self.request.user._type == 'ADMIN'
    def get_queryset(self):
        qs = super().get_queryset()
        print(qs.first().date)
        date = self.request.GET.get('date')#for custom date filter django_filter didnt work for sum reason
        if date:
            date_dt = make_aware(datetime.strptime(date, '%m/%d/%Y'))#convert sting date to datetime #makeaware is making aware about timezone
            qs = qs.filter(date__lte=date_dt)#filtering
        return qs.order_by('-id')

class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['contact','remarks']
    template_name = "inventory/small-form.html"
    def get_form(self, form_class=None):
        form = super(TransactionUpdateView, self).get_form(form_class)
        form.fields['remarks'].widget = SummernoteWidget()
        return form
    def test_func(self):
        return self.request.user._type == 'ADMIN'

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
        if qty <= 0:
            messages.warning(request, 'Quantity must be greater than 0.')
            return render(request, "inventory/small-form.html", context) 
        paid = int(request.POST.get('paid'))
        item = Item.objects.get(id=item)
        item.quantity = item.quantity-qty
        if item.quantity < 0:
            messages.warning(request, "Not Enough Stock To Sell")
            return render(request, "inventory/small-form.html", context)
        item.save()
        form.instance._type = 'STOCK OUT'
        trans = form.save()
        Payment.objects.create(transaction = trans, amount = paid)
        return redirect("inventory:items-list")
    return render(request, "inventory/small-form.html", context)

class CreditTransactionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CreditTransaction
    template_name = "inventory/cr_transactions.html"
    context_object_name = 'transactions'
    paginate_by=50
    def test_func(self):
        return self.request.user._type == 'ADMIN'
    def get_queryset(self):
        qs = super().get_queryset()
        sts = self.request.GET.get('state')
        if sts=='balanced':
            qs = qs.filter(balanced=True)
        elif sts=='unbalanced':
            qs = qs.filter(balanced=False)
        return qs

class CreditTransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CreditTransaction
    fields = ['contact','remarks']
    template_name = "inventory/small-form.html"
    def get_form(self, form_class=None):
        form = super(CreditTransactionUpdateView, self).get_form(form_class)
        form.fields['remarks'].widget = SummernoteWidget()
        return form
    def test_func(self):
        return self.request.user._type == 'ADMIN'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Update Transaction Info'
        return context
    
    def get_success_url(self):
        return reverse('inventory:credit-transactions')

@allowed_users(allowed_types = ['ADMIN'])
def DebitTransactionPaymentCreateView(request):
    form = DebitPaymentForm()
    context = {}
    context['form'] = form
    context['header'] = "Add Payment for Stock In (Bought Stocks)"
    if request.method=="POST":
        trans = request.POST.get('transaction')
        amt = int(request.POST.get('amount'))
        trans = DebitTransaction.objects.get(id=trans)
        trans.paid = trans.paid + amt
        if amt > trans.remaining_payment:
            messages.warning(request, "Paid Amount Cannot Be Greater than Remaining Payment")
            return render(request, "inventory/small-form.html", context)
        trans.save()
        Payment.objects.create(transaction = trans, amount = amt)
        # return reverse("inventory:debit-transactions")
    return render(request, "inventory/small-form.html", context)

@allowed_users(allowed_types = ['ADMIN'])
def CreditTransactionPaymentCreateView(request):
    form = CreditPaymentForm
    context = {}
    context['form'] = form
    context['header'] = "Add Payment for Stock Out (Sold Stocks)"
    if request.method=="POST":
        trans = request.POST.get('transaction')
        amt = int(request.POST.get('amount'))
        trans = CreditTransaction.objects.get(id=trans)
        trans.paid = trans.paid + amt
        if amt > trans.remaining_payment:
            messages.warning(request, "Paid Amount Cannot Be Greater than Remaining Payment")
            return render(request, "inventory/small-form.html", context)
        trans.save()
        Payment.objects.create(transaction = trans, amount = amt)
        # return reverse("inventory:debit-transactions")
    return render(request, "inventory/small-form.html", context)

class DebitPaymentListView(ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = "inventory/dr-payments.html"
    paginate_by=50
    queryset = Payment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Stock In Payments'
        return context

    def get_queryset(self):
        qs = super().get_queryset().filter(transaction___type="STOCK IN")
        sts = self.request.GET.get('state')
        if sts=='balanced':
            qs = qs.filter(transaction__balanced=True)
        elif sts=='unbalanced':
            qs = qs.filter(transaction__balanced=False)
        return qs.order_by('-id')

class CreditPaymentListView(ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = "inventory/dr-payments.html"
    paginate_by=50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Stock Out Payments'
        return context
    
    def get_queryset(self):
        qs = super().get_queryset().filter(transaction___type="STOCK OUT")
        sts = self.request.GET.get('state')
        if sts=='balanced':
            qs = qs.filter(transaction__balanced=True)
        elif sts=='unbalanced':
            qs = qs.filter(transaction__balanced=False)
        return qs.order_by('-id')

class QuickPaymentCreateView(CreateView):
    model = Payment
    fields = ['amount']
    template_name = "inventory/small-form.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_id = self.kwargs.get('pk')
        Trans = get_object_or_404(Transaction, id = obj_id)
        context["object"] = Trans
        return context
    def form_valid(self, form, *args, **kwargs):
        t_id =  self.kwargs.get('pk') #transaction id
        transaction = get_object_or_404(Transaction, id = t_id)
        form.instance.transaction = transaction
        amt = float(form.data['amount'])
        if transaction.remaining_payment >= amt:
            transaction.paid += amt
            transaction.save()
        else:
            messages.warning(self.request, "Payment amount cant be more than Remaining amount.")
            return redirect(reverse("inventory:quick-payment", kwargs={'pk':t_id}))
        form.save()
        return redirect(reverse('inventory:debit-transactions'))
    def get_success_url(self):
        return redirect(reverse('inventory:debit-transactions'))