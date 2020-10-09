from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField, HyperlinkedIdentityField
from rest_framework import serializers
from .models import Category, Item, Payment, DebitTransaction, Transaction, CreditTransaction
from django.db.models import Count
from django.urls import reverse

class PaymentSerializer(ModelSerializer):
    vendor_client = SerializerMethodField()
    transaction = SerializerMethodField()
    date = SerializerMethodField()
    balanced = SerializerMethodField()
    trans_id = SerializerMethodField()
    add_pay_url = SerializerMethodField() #i was lazy so i didnt made custom hyperlink serializers
    view_update_trans_url = SerializerMethodField()
    class Meta:
        model = Payment
        fields = ('transaction','amount','date', 'id', 'vendor_client', 'add_pay_url', 'view_update_trans_url', 'balanced', 'trans_id')
    def get_vendor_client(self, obj):
        return obj.transaction.vendor_client
    def get_transaction(self, obj):
        return str(obj.transaction)
    def get_add_pay_url(self, obj):
        return obj.transaction.get_absolute_url()
    def get_view_update_trans_url(self, obj):
        return str(reverse('inventory:transaction-update', kwargs={'pk':obj.transaction.id}))
    def get_date(self, obj):
        return timezone.localtime(obj.date).strftime("%b. %d, %Y")
    def get_balanced(self, obj):
        return obj.transaction.balanced
    def get_trans_id(self, obj):
        return obj.transaction.id

class CategoryChartSerializer(ModelSerializer):
    items_count = serializers.SerializerMethodField(read_only=True)

    def get_items_count(self, obj):
        return sum([i.quantity for i in obj.categories.all()])#here categories is related_name on Item Model

    class Meta:
        model = Category
        fields = ('name','items_count',)

class ItemQuantitySerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('name','quantity','selling_price','brand', 'id')

from datetime import datetime
from django.utils import timezone
class TransactionSerializer(ModelSerializer):
    pay_url = HyperlinkedIdentityField(view_name='inventory:quick-payment')
    update_url = HyperlinkedIdentityField(view_name='inventory:transaction-update')
    payable = SerializerMethodField()
    remaining_payment = SerializerMethodField()
    item = SerializerMethodField()
    date = SerializerMethodField()
    item_id = SerializerMethodField()
    class Meta:
        model = Transaction
        fields = ['id', 'vendor_client', 'date', 'item_id', 'item','_type', 'quantity', 'paid', 'payable', 'remaining_payment', 'pay_url', 'balanced', 'cost', 'update_url', 'is_debit']
    def get_payable(self, obj):
        return obj.quantity * obj.cost
    def get_remaining_payment(self, obj):
        return self.get_payable(obj) - obj.paid
    def get_item(self, obj):
        return obj.item.name
    def get_date(self, obj):
        return timezone.localtime(obj.date).strftime("%b. %d, %Y")
        # return obj.date.date()
        # return datetime.strptime(obj.date).date()
    def get_item_id(self, obj):
        return obj.item.id

class ItemDetailSerializer(ModelSerializer):
    category = SerializerMethodField()
    unpaid_dr_trans = SerializerMethodField()
    unpaid_cr_trans = SerializerMethodField()
    class Meta:
        model = Item
        fields = ['id','name', 'brand', 'category', 'quantity', 'selling_price', 'cost_price', 'unpaid_dr_trans', 'unpaid_cr_trans']
    def get_category(self, obj):
        return obj.category.name
    def get_unpaid_dr_trans(self, obj):
         dr_trans_qs = DebitTransaction.objects.unpaid().filter(item = obj)
         dr_trans = TransactionSerializer(dr_trans_qs, many=True, context=self.context).data
         return dr_trans
    def get_unpaid_cr_trans(self, obj):
         cr_trans_qs = CreditTransaction.objects.unpaid().filter(item = obj)
         cr_trans = TransactionSerializer(cr_trans_qs, many=True, context=self.context).data
         return cr_trans
    
