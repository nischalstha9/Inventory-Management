from django.shortcuts import render, reverse
from .forms import ItemFormSet, InvoiceForm
from .models import Invoice, InvoiceItem
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class InvoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Invoice
    fields = '__all__'
    template_name = 'invoice/create_invoice.html'

    def test_func(self):
        return self.request.user._type == 'ADMIN'

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['inv_item_form'] = ItemFormSet(
                self.request.POST, prefix='invoiceitem_set')
        else:
            context['inv_item_form'] = ItemFormSet(prefix='invoiceitem_set')
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['inv_item_form']
        print(formset.data)
        # self.buyer = form.save()
        # if self.buyer.id != None:
        #     if form.is_valid() and formset.is_valid():
        #         formset.instance = self.buyer
        #         # formset.save()
        # return super().form_valid(form)

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     formset = context['inv_item_form']
        # self.object = form.save()
        # if self.object.id != None:
        #     if form.is_valid() and formset.is_valid():
        #         formset.instance = self.object
        #         # formset.save()
        # return super().form_valid(form)

    def save(self):
        pass
    
    def get_success_url(self):
        return reverse('invoice:invoice-detail', self.id)


class InvoiceListView(ListView):
    model = Invoice
    template_name = "invoice/invoice_list.html"
    context_object_name = 'invoices'
    paginate_by = 50

class InvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Invoice
    template_name = "invoice/invoice_detail.html"
    context_object_name = 'invoice'

    def test_func(self):
        return self.request.user._type == 'ADMIN'




