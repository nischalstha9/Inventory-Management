from django.urls import path, include
from .views import index, ItemCreationVIew, ItemListView, ItemUpdateVIew, add_to_inventory, DebitTransactionListView, DebitTransactionUpdateView
from .api_views import ItemQuantity

app_name = 'inventory'
urlpatterns = [
    path("item-quantity/", ItemQuantity.as_view(), name="cat-cnt"), 

    path("", ItemListView.as_view() , name="items-list"),
    path("new/", ItemCreationVIew.as_view(), name="new-item"),
    path("<int:pk>/update/", ItemUpdateVIew.as_view(), name="item-update"),

    path("add-stock/", add_to_inventory, name="add-stock"),
    path("transactions/", DebitTransactionListView.as_view(), name="transactions"),
    path("transactions/<int:pk>/update/", DebitTransactionUpdateView.as_view(), name="transaction-update"),
]