from django.urls import path, include
from .views import home

app_name = 'main'
urlpatterns = [
    path("", home, name="home")
]