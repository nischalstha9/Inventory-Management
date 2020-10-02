from django.forms import ModelForm
from .models import Item, Category, DebitTransaction, CreditTransaction, DebitTransactionInfo, CreditTransactionInfo
from django.core.exceptions import ValidationError

class ItemCreationForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ("cost_price", "quantity")

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
    class Meta:
        model = DebitTransaction
        fields = '__all__'
        exclude = ['_type']

class DebitTransactionInfoForm(ModelForm): 
    class Meta:
        model = DebitTransactionInfo
        fields = '__all__'
        exclude = ['transaction']

class CreditTransactionForm(ModelForm): 
    class Meta:
        model = CreditTransaction
        fields = '__all__'
        exclude = ['_type']

class CreditTransactionInfoForm(ModelForm): 
    class Meta:
        model = CreditTransactionInfo
        fields = '__all__'
        exclude = ['transaction']