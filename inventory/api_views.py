from .models import Item, Category, Transaction
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CategoryChartSerializer, ItemQuantitySerializer, TransactionSerializer, ItemDetailSerializer

class CategoryNcount(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryChartSerializer

class ItemQuantity(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemQuantitySerializer

class TransactionDetailAPIView(RetrieveAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

class ItemDetailAPIView(RetrieveAPIView):
    serializer_class = ItemDetailSerializer
    queryset = Item.objects.all()
    