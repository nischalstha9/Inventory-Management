from django.urls import path, include
from .views import index, ItemCreationVIew, ItemListView, ItemUpdateVIew, add_to_inventory, DebitTransactionListView, DebitTransactionUpdateView, sell_from_inventory, CreditTransactionListView, CreditTransactionUpdateView, CreditTransactionPaymentCreateView, DebitTransactionPaymentCreateView, DebitPaymentListView, CreditPaymentListView, CategoryCreateView
from .api_views import ItemQuantity, TransactionDetailAPIView, ItemDetailAPIView

app_name = 'inventory'
urlpatterns = [
    #api urls
    path("item/<int:pk>/", ItemDetailAPIView.as_view(), name="item-detail-api"),
    path("transaction/<int:pk>/", TransactionDetailAPIView.as_view(), name="transaction-detail-api"),
    path("item-quantity/", ItemQuantity.as_view(), name="cat-cnt"), 
    ############################################DIVIDER############################################

    path("category/new/", CategoryCreateView.as_view() , name="new-category"),

    path("", ItemListView.as_view() , name="items-list"),
    path("new/", ItemCreationVIew.as_view(), name="new-item"),
    path("<int:pk>/update/", ItemUpdateVIew.as_view(), name="item-update"),

    path("add-stock/", add_to_inventory, name="add-stock"),
    path("sell-stock/", sell_from_inventory, name="sell-stock"),
    path("transactions/debit/", DebitTransactionListView.as_view(), name="debit-transactions"),
    path("transactions/dr/<int:pk>/update/", DebitTransactionUpdateView.as_view(), name="dr-transaction-update"),

    path("transactions/credit/", CreditTransactionListView.as_view(), name="credit-transactions"),
    path("transactions/cr/<int:pk>/update/", CreditTransactionUpdateView.as_view(), name="cr-transaction-update"),

    path("payment/dr/new/", DebitTransactionPaymentCreateView, name="dr-payment-create"),
    path("payment/cr/new/", CreditTransactionPaymentCreateView, name="cr-payment-create"),
    path("payments/dr/", DebitPaymentListView.as_view(), name="dr-payments"),
    path("payments/cr/", CreditPaymentListView.as_view(), name="cr-payments"),
    
    
]