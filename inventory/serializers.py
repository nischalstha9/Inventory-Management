from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField, HyperlinkedIdentityField
from rest_framework import serializers
from .models import Category, Item, Payment, DebitTransaction, Transaction, CreditTransaction
from django.db.models import Count

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
        fields = ('name','quantity','selling_price','brand')

from datetime import datetime
from django.utils import timezone
class TransactionSerializer(ModelSerializer):
    pay_url = HyperlinkedIdentityField(view_name='inventory:quick-payment')
    update_url = HyperlinkedIdentityField(view_name='inventory:transaction-update')
    payable = SerializerMethodField()
    remaining_payment = SerializerMethodField()
    item = SerializerMethodField()
    date = SerializerMethodField()
    transaction_id = SerializerMethodField()
    class Meta:
        model = Transaction
        fields = ['id', 'vendor_client', 'date', 'transaction_id', 'item','_type', 'quantity', 'paid', 'payable', 'remaining_payment', 'pay_url', 'balanced', 'cost', 'update_url', 'is_debit']
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
    def get_transaction_id(self, obj):
        return obj.id


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
    
