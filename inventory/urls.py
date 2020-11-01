from django.urls import path, include
from .views import index, ItemCreationVIew, ItemListView, ItemUpdateVIew, add_to_inventory, DebitTransactionListView, TransactionUpdateView, sell_from_inventory, CreditTransactionListView, CreditTransactionPaymentCreateView, DebitTransactionPaymentCreateView, DebitPaymentListView, CreditPaymentListView, CategoryCreateView, ItemDeleteView, QuickPaymentCreateView, TransactionListView,PaymentListView, OrderListView, OrderDetailView, CarouselListView
from .api_views import ItemQuantity, TransactionDetailAPIView, ItemDetailAPIView,TransactionListAPIView, PaymentListAPIView, PaymentDetailAPIView, dashboard_view, OrdersListAPIView, carousel_info_view

app_name = 'inventory'
urlpatterns = [
    #api urls
    path("dashboard/", dashboard_view, name="dashboard-api"),
    path("item/<int:pk>/", ItemDetailAPIView.as_view(), name="item-detail-api"),
    path("transaction/<int:pk>/", TransactionDetailAPIView.as_view(), name="transaction-detail-api"),
    path("payment/<int:pk>/", PaymentDetailAPIView.as_view(), name="payment-detail-api"),
    path("item-quantity/", ItemQuantity.as_view(), name="cat-cnt"), 
    path("api/transactions/", TransactionListAPIView.as_view(), name="transactions-api-list"), 
    path("api/payments/", PaymentListAPIView.as_view(), name="payments-api-list"), 
    path("api/orders/", OrdersListAPIView.as_view(), name="orders-api-list"), 
    ############################################DIVIDER############################################

    path("category/new/", CategoryCreateView.as_view() , name="new-category"),

    path("", ItemListView.as_view() , name="items-list"),
    path("new/", ItemCreationVIew.as_view(), name="new-item"),
    path("<int:pk>/update/", ItemUpdateVIew.as_view(), name="item-update"),
    path("<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete"),

    path("add-stock/", add_to_inventory, name="add-stock"),
    path("sell-stock/", sell_from_inventory, name="sell-stock"),
    path("transactions/all/", TransactionListView, name="transactions-list"),
    path("transactions/debit/", DebitTransactionListView.as_view(), name="debit-transactions"),
    path("transactions/<int:pk>/update/", TransactionUpdateView.as_view(), name="transaction-update"),

    path("transactions/credit/", CreditTransactionListView.as_view(), name="credit-transactions"),
    
    path("transactions/<int:pk>/quickpay/", QuickPaymentCreateView.as_view(), name="quick-payment"),


    path("payment/all/", PaymentListView, name="payments-list"),
    path("payment/dr/new/", DebitTransactionPaymentCreateView, name="dr-payment-create"),
    path("payment/cr/new/", CreditTransactionPaymentCreateView, name="cr-payment-create"),
    path("payments/dr/", DebitPaymentListView.as_view(), name="dr-payments"),
    path("payments/cr/", CreditPaymentListView.as_view(), name="cr-payments"),

    path("orders/", OrderListView, name="orders-list"),
    path("orders/<int:pk>/", OrderDetailView, name="order-detail"),
    path("carousels/", CarouselListView.as_view(), name="carousels-list"),
    path("carousels/<int:pk>/", carousel_info_view, name="carousels-api"),


    
    
]