from .models import Item, Category
from rest_framework.generics import ListAPIView
from .serializers import CategoryChartSerializer, ItemQuantitySerializer

class CategoryNcount(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryChartSerializer

class ItemQuantity(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemQuantitySerializer

# class UnpaidDebitInfoListView(ListAPIView):
#     queryset = DebitTransactionInfo.objects.unpaid()
#     serializer_class = DebitTransactionSerializer