from django.forms import ModelForm, Form
from django import forms
from .models import Item, Category, DebitTransaction, CreditTransaction, Payment, Transaction
from django.core.exceptions import ValidationError

class ItemCreationForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ("cost_price", "quantity", 'selling_price')

    def clean_qty(self):
        qty = self.cleaned_data['quantity']
        if qty < 0:
            raise ValidationError("Quantity cannot be less than 0.")
        return qty
    def clean_cp(self):
        cp = self.cleaned_data['cost_price']
        if cp <= 0:
            raise ValidationError("Cost Price cannot be 0.")
        return cp
    def clean_qty(self):
        sp = self.cleaned_data['selling_price']
        if sp <= 0:
            raise ValidationError("Selling Price cannot be 0")
        return sp

class DebitTransactionForm(ModelForm):
    selling_price = forms.IntegerField(initial=0, required=True)
    class Meta:
        model = DebitTransaction
        fields = '__all__'
        exclude = ['_type']
        labels = {
            'vendor_client':'Vendor'
        }

class CreditTransactionForm(ModelForm): 
    class Meta:
        model = CreditTransaction
        fields = '__all__'
        exclude = ['_type']
        labels = {
            'vendor_client':'Client',
            'cost':'Price Per Quantity Unit'
        }
    def __init__(self, *args, **kwargs):
        super(CreditTransactionForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['item'].queryset = Item.objects.filter(quantity__gt=0)

class DebitPaymentForm(forms.Form):
    transaction = forms.ModelChoiceField(queryset = DebitTransaction.objects.unpaid())
    amount = forms.IntegerField(required=True)
    
class CreditPaymentForm(forms.Form):
    transaction = forms.ModelChoiceField(queryset = CreditTransaction.objects.unpaid())
    amount = forms.IntegerField(required=True)
    
