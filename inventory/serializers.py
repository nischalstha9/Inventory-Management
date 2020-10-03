from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from rest_framework import serializers
from .models import Category, Item, Payment, DebitTransaction, Transaction
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
        fields = ('name','quantity')

from datetime import datetime
from django.utils import timezone
class TransactionSerializer(ModelSerializer):
    payable = SerializerMethodField()
    remaining_payment = SerializerMethodField()
    item = SerializerMethodField()
    date = SerializerMethodField()
    transaction_id = SerializerMethodField()
    class Meta:
        model = Transaction
        fields = ['date', 'transaction_id', 'item', 'vendor_client', '_type', 'quantity', 'paid', 'payable', 'remaining_payment']
    def get_payable(self, obj):
        return obj.quantity * obj.cost
    def get_remaining_payment(self, obj):
        return obj.paid - self.get_payable(obj)
    def get_item(self, obj):
        return obj.item.name
    def get_date(self, obj):
        # return obj.date.date()
        # return datetime.strptime(obj.date).date()
        return timezone.localtime(obj.date).strftime("%b. %d, %Y")
    def get_transaction_id(self, obj):
        return obj.id


class ItemDetailSerializer(ModelSerializer):
    category = SerializerMethodField()
    class Meta:
        model = Item
        fields = ['id','name', 'brand', 'category', 'quantity', 'selling_price']
    def get_category(self, obj):
        return obj.category.name