from django.urls import path, include
from .views import index

app_name = 'inventory'
urlpatterns = [
    path("", index , name="home")
]