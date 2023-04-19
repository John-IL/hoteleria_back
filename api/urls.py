
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.LoginApi.as_view(), name="login"),
    path('logout', views.logout, name="logout"),
    path('user/list', views.viewGetUsers, name="list-users"),
    path('user/register', views.viewRegisterUser, name="register-user"),
    path('user/update', views.viewUpdateUser, name="update-user"),

    path('roles/list', views.viewGetRoles, name="list-roles"),

    path('document-types/list', views.viewGetDocumentTypes, name="list-document-types"),

    path('countries/list', views.viewGetCountries, name="list-countries"),


    path('promotion/register', views.viewRegisterPromotion, name="register-promotion"),
]