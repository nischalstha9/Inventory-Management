from .models import Item, Category, Transaction, Payment
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CategoryChartSerializer, ItemQuantitySerializer, TransactionSerializer, ItemDetailSerializer, PaymentSerializer
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from django_filters import rest_framework as filters

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
    filter_backends = [SearchFilter]
    search_fields = ['name','category__name','brand']
    # pagination_class = StandardResultsSetPagination

class TransactionDetailAPIView(RetrieveAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsStaff]

class PaymentDetailAPIView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsStaff]

class ItemDetailAPIView(RetrieveAPIView):
    serializer_class = ItemDetailSerializer
    queryset = Item.objects.all()
    permission_classes = [IsStaff]

class TransactionListAPIView(ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsStaff]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = ()
    search_fields = ['vendor_client', 'item__name',]
    pagination_class = StandardResultsSetPagination
    filterset_fields = {
    'date':['gte', 'lte', 'date__range'],'balanced':['exact'], '_type':['exact'], 'id':['exact']}

class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsStaff]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    search_fields = ['transaction__vendor_client', 'transaction__item__name',]
    pagination_class = StandardResultsSetPagination
    filterset_fields = {
    'date':['date__range'],'transaction__balanced':['exact'], 'transaction___type':['exact'], 'transaction__id':['exact']}