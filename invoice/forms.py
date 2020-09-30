from django import forms
from .models import Invoice, InvoiceItem

ItemFormSet = forms.inlineformset_factory(Invoice, InvoiceItem,  fields = ('item', 'quantity', 'sp'))

# class InvoiceForm(forms.Form):
#     Buyer_name = forms.CharField(label='Buyer name', max_length=128)


class InvoiceForm(forms.ModelForm):  
    class Meta:
        model = Invoice
        fields = ('buyer_name',)

class InvoiceItemForm(forms.ModelForm):
    
    class Meta:
        model = InvoiceItem
        fields = ("item",'quantity', 'sp')


