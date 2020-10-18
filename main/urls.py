from django.urls import path, include
from .views import home,ItemListView, ItemDetailView, cart
from .api_view import create_order,api_cart

app_name = 'main'
urlpatterns = [
    path("administration/", home, name="admin-home"),
    path("", ItemListView.as_view(), name="home"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("cart/", cart, name="cart"),
    ##########APIVIEW##################
    path("create-order/", create_order, name="api-create-order"),
    path("cart-update/", api_cart, name="api-cart-form"),
]