
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.LoginApi.as_view(), name="login"),
    path('logout', views.logout, name="logout"),
    path('products', views.ProductApi.as_view(), name='products'),
    path('products-category', views.ProductCategoryApi.as_view(), name='products-category'),
    path('products-family', views.ProductFamilyApi.as_view(), name='products-family')
]