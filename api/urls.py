
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.LoginApi.as_view(), name="login"),
    path('logout', views.logout, name="logout"),
    path('users/list', views.viewGetUsers, name="list-users"),
]