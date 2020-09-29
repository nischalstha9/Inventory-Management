from django.urls import path, include
from .views import index, ItemCreationVIew, ItemListView, ItemUpdateVIew, CategoryNcount

app_name = 'inventory'
urlpatterns = [
    path("cat_Count/", CategoryNcount.as_view(), name="cat-cnt"), 

    path("", ItemListView.as_view() , name="items-list"),
    path("new/", ItemCreationVIew.as_view(), name="new-item"),
    path("<int:pk>/update/", ItemUpdateVIew.as_view(), name="item-update"),
]