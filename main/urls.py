from django.urls import path, include
from .views import home,ItemListView, ItemDetailView, cart, CheckoutDataCreateView, MyOrderListView, CategoryItemListView
from .api_view import create_order,api_cart, CarouselImageDeleteView

app_name = 'main'
urlpatterns = [
    path("administration/", home, name="admin-home"),
    path("", ItemListView.as_view(), name="home"),
    path("category/<int:pk>/", CategoryItemListView.as_view(), name="category-item-list"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("cart/", cart, name="cart"),
    path("checkout/", CheckoutDataCreateView.as_view(), name="checkout-form"),
    ##########APIVIEW##################
    path("create-order/", create_order, name="api-create-order"),
    path("cart-update/", api_cart, name="api-cart-form"),
    path("myorders/", MyOrderListView.as_view(), name="my-orders"),

    path("carousels/<int:pk>/delete", CarouselImageDeleteView, name="carousel-image-del"),


]