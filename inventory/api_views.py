from .models import Item, Category, Transaction, Payment,DebitTransaction,CreditTransaction
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CategoryChartSerializer, ItemQuantitySerializer, TransactionSerializer, ItemDetailSerializer, PaymentSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from django.utils import timezone

class IsStafforAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user._type in ['ADMIN', 'STAFF']
        return False
    
class IsAdmin(permissions.BasePermission):
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
    permission_class = [IsStafforAdmin]

class PaymentDetailAPIView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_class = [IsStafforAdmin]

class ItemDetailAPIView(RetrieveAPIView):
    serializer_class = ItemDetailSerializer
    queryset = Item.objects.all()
    permission_class = [IsStafforAdmin]

class TransactionListAPIView(ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_class = [IsStafforAdmin]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = ()
    search_fields = ['vendor_client', 'item__name',]
    pagination_class = StandardResultsSetPagination
    filterset_fields = {
    'date':['gte', 'lte', 'date__range'],'balanced':['exact'], '_type':['exact'], 'id':['exact']}

class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_class = [IsStafforAdmin]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    search_fields = ['transaction__vendor_client', 'transaction__item__name',]
    pagination_class = StandardResultsSetPagination
    filterset_fields = {
    'date':['date__range'],'transaction__balanced':['exact'], 'transaction___type':['exact'], 'transaction__id':['exact']}

@api_view(['GET'])
def dashboard_view(request):
    data = {}
    today_pay = Payment.objects.filter(date__date = timezone.now().date())
    today_dr_pays = [i.amount for i in today_pay.filter(transaction___type='STOCK IN')]
    today_cr_pays = [i.amount for i in today_pay.filter(transaction___type='STOCK OUT')]
    #actual workings
    today_dr_trans = DebitTransaction.objects.filter(date__date = timezone.now().date()).count()
    today_cr_trans = CreditTransaction.objects.filter(date__date = timezone.now().date()).count()
    today_pay_sent = sum(today_dr_pays)
    today_pay_receive = sum(today_cr_pays)
    today_highest_pay_sent = max(today_dr_pays or [1,2])
    today_highest_pay_received = max(today_cr_pays or [1,2])
    data['today_dr_trans'] = today_dr_trans
    data['today_cr_trans'] = today_cr_trans
    data['today_pay_recv'] = today_pay_receive
    data['today_pay_sent'] = today_pay_sent
    data['today_highest_pay_sent'] = today_highest_pay_sent
    data['today_highest_pay_received'] = today_highest_pay_received
    return Response(data)