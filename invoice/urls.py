from django.urls import path, include
from .views import InvoiceCreateView, InvoiceListView, InvoiceDetailView

app_name = 'invoice'
urlpatterns = [
    path("", InvoiceListView.as_view() , name="invoice-list"),
    path("new/", InvoiceCreateView.as_view(), name="new-invoice"),
    path("<int:pk>/", InvoiceDetailView.as_view(), name="invoice-detail"),
    # path("<int:pk>/update/", ItemUpdateVIew.as_view(), name="item-update"),
]