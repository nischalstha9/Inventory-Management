from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from rest_framework import serializers
from .models import Category, Item
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