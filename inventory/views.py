from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import ItemCreationForm, DebitTransactionForm, CreditTransactionForm, DebitPaymentForm, CreditPaymentForm,PaymentForm
from .models import Item, DebitTransaction, Category, CreditTransaction, Payment, Transaction, Carousel
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from django_filters.views import FilterView
from .filters import DebitTransactionFilter
from datetime import datetime
from django.utils.timezone import make_aware
from django_summernote.widgets import SummernoteWidget
from main.models import Order, OrderItem

#custom decorator for filtering permission
def allowed_users(allowed_types=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user._type in allowed_types:
                    return view_func(request, *args, **kwargs)
            else:
                return redirect(reverse('account_login'))
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
        return self.request.user._type in ['ADMIN', 'STAFF']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create New Category"
        context["header"] = "Create New Category"
        return context
    

class ItemCreationVIew(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ItemCreationForm
    template_name = 'inventory/big-form.html'
    success_url = "../"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create New Inventory Item"
        context["header"] = "Create New Inventory Item"
        return context
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']

class ItemListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Item
    template_name = "inventory/item_list.html"
    context_object_name = 'items'
    paginate_by = 50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Inventory Items List"
        return context
    
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']

class ItemUpdateVIew(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ItemCreationForm
    template_name = 'inventory/big-form.html'
    success_url = "../../"
    queryset = Item.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update Item - {self.object}"
        return context
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = "inventory/delete_item.html"
    def get_success_url(self):
        return reverse('inventory:items-list')
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Delete Item - {self.object}"
        return context
    


@allowed_users(allowed_types = ['ADMIN', 'STAFF'])
def add_to_inventory(request):
    context = {'header' : 'Add Stock'}
    form = DebitTransactionForm(request.POST or None)
    context['form']= form
    context['title']= "Add Stock"
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
        payment = Payment.objects.create(transaction = trans, amount=paid, base_payment=True)
        payment.save()
        return redirect("inventory:items-list")
    return render(request, "inventory/small-form.html", context)

@allowed_users(allowed_types = ['ADMIN', 'STAFF'])
def TransactionListView(request):
    context = {'title':'Transactions List'}
    return render(request, 'inventory/transactions.html', context)

@allowed_users(allowed_types = ['ADMIN', 'STAFF'])
def PaymentListView(request):
    context = {'title':'Payments List'}
    return render(request, 'inventory/payments.html', context)

class DebitTransactionListView(LoginRequiredMixin, UserPassesTestMixin, FilterView):
    model = DebitTransaction
    template_name = "inventory/dr_transactions.html"
    context_object_name = 'transactions'
    paginate_by=50
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']
    def get_queryset(self):
        qs = super().get_queryset()
        print(qs.first().date)
        date = self.request.GET.get('date')#for custom date filter django_filter didnt work for sum reason
        if date:
            date_dt = make_aware(datetime.strptime(date, '%m/%d/%Y'))#convert sting date to datetime #makeaware is making aware about timezone
            qs = qs.filter(date__lte=date_dt)#filtering
        return qs.order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Debit Transactions"
        return context
    

class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['quantity', 'contact', 'remarks']
    template_name = "inventory/small-form.html"
    def get_form(self, form_class=None):
        form = super(TransactionUpdateView, self).get_form(form_class)
        form.fields['remarks'].widget = SummernoteWidget()
        return form
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Transaction Info"
        context["header"] = 'Update Transaction Info'
        context['payments'] = Payment.objects.filter(transaction = self.object.pk)
        return context
    def get_success_url(self):
        return reverse('inventory:debit-transactions')
    def form_valid(self, form, *args, **kwargs):
        """Here object refers to form so we were getting item qty of form making errors"""
        obj_id = self.object.id
        obj = Transaction.objects.get(id=obj_id)
        item = obj.item
        n_qty = int(self.request.POST.get('quantity')) #new quantity from POST
        item.quantity = item.quantity - obj.quantity + n_qty
        item.save()
        form.save()
        return redirect(reverse('inventory:transaction-update', kwargs = {'pk':obj_id}))

@allowed_users(allowed_types = ['ADMIN', 'STAFF'])
def sell_from_inventory(request):
    context = {'header' : 'Sell Stock'}
    form = CreditTransactionForm(request.POST or None)
    context['title']= "Sell Stock"
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
        Payment.objects.create(transaction = trans, amount = paid, base_payment=True)
        return redirect("inventory:items-list")
    return render(request, "inventory/small-form.html", context)

class CreditTransactionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CreditTransaction
    template_name = "inventory/cr_transactions.html"
    context_object_name = 'transactions'
    paginate_by=50
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']
    def get_queryset(self):
        qs = super().get_queryset()
        sts = self.request.GET.get('state')
        if sts=='balanced':
            qs = qs.filter(balanced=True)
        elif sts=='unbalanced':
            qs = qs.filter(balanced=False)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Credit Transactions"
        return context

@allowed_users(allowed_types = ['ADMIN', 'STAFF'])
def DebitTransactionPaymentCreateView(request):
    form = DebitPaymentForm()
    context = {}
    context['form'] = form
    context['title'] = "Create Payment"
    context['header'] = "Add Payment for Stock In (Bought Stocks)"
    if request.method=="POST":
        trans = request.POST.get('transaction')
        amt = int(request.POST.get('amount'))
        amt2 = int(request.POST.get('amount_2'))
        trans = DebitTransaction.objects.get(id=trans)
        trans.paid = trans.paid + amt
        if amt > trans.remaining_payment and amt!=amt2:
            messages.warning(request, "Both Payment amount should match and cannot be more than Remaining amount.")
            return render(request, "inventory/small-form.html", context)
        trans.save()
        Payment.objects.create(transaction = trans, amount = amt)
    return render(request, "inventory/small-form.html", context)

@allowed_users(allowed_types = ['ADMIN', 'STAFF'])
def CreditTransactionPaymentCreateView(request):
    form = CreditPaymentForm
    context = {}
    context['form'] = form
    context['title'] = "Create Payment"
    context['header'] = "Add Payment for Stock Out (Sold Stocks)"
    if request.method=="POST":
        trans = request.POST.get('transaction')
        amt = int(request.POST.get('amount'))
        amt2 = int(request.POST.get('amount_2'))
        trans = CreditTransaction.objects.get(id=trans)
        trans.paid = trans.paid + amt
        if amt > trans.remaining_payment and amt != amt2:
            messages.warning(request, "Both Payment amount should match and cannot be more than Remaining amount.")
            return render(request, "inventory/small-form.html", context)
        trans.save()
        Payment.objects.create(transaction = trans, amount = amt)
    return render(request, "inventory/small-form.html", context)

class DebitPaymentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = "inventory/dr-payments.html"
    paginate_by=50
    queryset = Payment.objects.all()
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Stock In Payments'
        context['title'] = "Payments Created for Stock Bought"
        return context
    def get_queryset(self):
        qs = super().get_queryset().filter(transaction___type="STOCK IN")
        sts = self.request.GET.get('state')
        if sts=='balanced':
            qs = qs.filter(transaction__balanced=True)
        elif sts=='unbalanced':
            qs = qs.filter(transaction__balanced=False)
        return qs.order_by('-id')

class CreditPaymentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = "inventory/dr-payments.html"
    paginate_by=50
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = 'Stock Out Payments'
        context['title'] = "Payments Created for Stock Sold"
        return context    
    def get_queryset(self):
        qs = super().get_queryset().filter(transaction___type="STOCK OUT")
        sts = self.request.GET.get('state')
        if sts=='balanced':
            qs = qs.filter(transaction__balanced=True)
        elif sts=='unbalanced':
            qs = qs.filter(transaction__balanced=False)
        return qs.order_by('-id')

@allowed_users(allowed_types = ['ADMIN', 'STAFF'])
def OrderListView(request):
    context = {'title':'Orders List'}
    return render(request, 'inventory/orders.html', context)

from django import forms
class StatusChangeForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

@allowed_users(allowed_types = ['ADMIN', 'STAFF'])
def OrderDetailView(request, pk):
    context = {}
    order = get_object_or_404(Order, pk = pk)
    order_items = order.items.all()
    context['header'] = f"Order Detail of {order.user}"
    context['order'] = order
    form = StatusChangeForm(request.POST or None, instance=order)
    context['form'] = form
    context['order_items'] = order_items
    if request.method=='POST':
        sts = form.data.get('status')
        if sts != 'NO' and order.status != 'S':
            order.status = sts
            order.save()
            if sts == 'S':
                for i in order_items:
                    item_ = i.item
                    item_.quantity -= i.quantity
                    item_.save()
                    trans = Transaction.objects.create(_type="STOCK OUT",vendor_client = str(f"{order.user.first_name} {order.user.last_name}"), item = item_, quantity = i.quantity, cost = item_.selling_price, paid = item_.selling_price, remarks=order.checkout.remarks, contact = order.checkout.contact)
                    trans.save()
                    pay = Payment.objects.create(transaction = trans, amount = item_.selling_price, base_payment=True)
                    pay.save()
            messages.success(request, 'Order Status Updated!')
        else:
            messages.warning(request, 'Cannot Set Order Status Contact Admin')
    return render(request, 'inventory/order_detail.html', context)

class QuickPaymentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = PaymentForm
    template_name = "inventory/small-form.html"
    def test_func(self):
        return self.request.user._type in ['ADMIN', 'STAFF']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_id = self.kwargs.get('pk')
        Trans = get_object_or_404(Transaction, id = obj_id)
        context["object"] = Trans
        context["payments"] = Payment.objects.filter(transaction = Trans)
        context["header"] = f"Add Payment for {Trans}"
        context["title"] = f"Create Payment for {Trans}"
        return context
    def form_valid(self, form, *args, **kwargs):
        t_id =  self.kwargs.get('pk') #transaction id
        transaction = get_object_or_404(Transaction, id = t_id)
        form.instance.transaction = transaction
        amt = float(form.data['amount'])
        amt2 = float(form.data['amount_2'])
        if transaction.remaining_payment >= amt and amt == amt2:
            transaction.paid += amt
            transaction.save()
        else:
            messages.warning(self.request, "Both Payment amount should match and cannot be more than Remaining amount.")
            return redirect(reverse("inventory:quick-payment", kwargs={'pk':t_id}))
        form.save()
        return redirect(reverse('inventory:payments-list'))
    def get_success_url(self):
        return redirect(reverse('inventory:payments-list'))

class CarouselListView(ListView):
    model = Carousel
    context_object_name = 'carousels'
    template_name = "inventory/carousel_list.html"