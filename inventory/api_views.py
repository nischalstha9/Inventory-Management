from .models import Item, Category, Transaction
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CategoryChartSerializer, ItemQuantitySerializer, TransactionSerializer, ItemDetailSerializer
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class IsStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user._type in ['ADMIN']
        return False

class CategoryNcount(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryChartSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class ItemQuantity(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemQuantitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','category__name','brand']
    # pagination_class = StandardResultsSetPagination

class TransactionDetailAPIView(RetrieveAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsStaff]

class ItemDetailAPIView(RetrieveAPIView):
    serializer_class = ItemDetailSerializer
    queryset = Item.objects.all()
    permission_classes = [IsStaff]
    