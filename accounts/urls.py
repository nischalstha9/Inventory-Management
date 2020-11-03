from django.urls import path
from .views import UserCreateView, UserUpdateView, UserListAPIView, userlistview

app_name='accounts'
urlpatterns = [
    path("new-user/", UserCreateView.as_view(), name="new-user"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("api/users/", UserListAPIView.as_view(), name="users-api-list"),
    path("users/", userlistview, name="users-list"),    
]