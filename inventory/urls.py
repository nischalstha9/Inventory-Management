from django.urls import path, include
from .views import index, ItemCreationVIew, ItemListView, ItemUpdateVIew, add_to_inventory, DebitTransactionListView, DebitTransactionUpdateView, sell_from_inventory, CreditTransactionListView, CreditTransactionUpdateView
from .api_views import ItemQuantity

app_name = 'inventory'
urlpatterns = [
    path("item-quantity/", ItemQuantity.as_view(), name="cat-cnt"), 

    path("", ItemListView.as_view() , name="items-list"),
    path("new/", ItemCreationVIew.as_view(), name="new-item"),
    path("<int:pk>/update/", ItemUpdateVIew.as_view(), name="item-update"),

    path("add-stock/", add_to_inventory, name="add-stock"),
    path("sell-stock/", sell_from_inventory, name="sell-stock"),
    path("transactions/debit/", DebitTransactionListView.as_view(), name="debit-transactions"),
    path("transactions/<int:pk>/update/", DebitTransactionUpdateView.as_view(), name="dr-transaction-update"),

    path("transactions/credit/", CreditTransactionListView.as_view(), name="credit-transactions"),
    path("transactions/cr/<int:pk>/update/", CreditTransactionUpdateView.as_view(), name="cr-transaction-update"),
    
]