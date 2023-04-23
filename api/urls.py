
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

    # promotions
    path('promotion/register', views.viewRegisterPromotion, name="register-promotion"),
    path('promotion/update', views.viewUpdatePromotion, name="update-promotion"),
    path('promotion/list', views.viewGetPromotions, name="list-promotion"),

    # category
    path('category/register', views.viewRegisterCategory, name="register-category"),
    path('category/update', views.viewUpdateCategory, name="update-category"),
    path('category/list', views.viewGetCategories, name="list-category"),

    # banner
    path('banner/register', views.viewRegisterBanner, name="register-banner"),
    path('banner/update', views.viewUpdateBanner, name="update-banner"),
    path('banner/list', views.viewGetBanners, name="list-banner"),

    # client
    path('client/register', views.viewRegisterClient, name="register-client"),
    path('client/update', views.viewUpdateClient, name="update-client"),
    path('client/list', views.viewGetClients, name="list-client"),

    # promotion
    path('promotion/register', views.viewRegisterPromotion, name="register-promotion"),
    path('promotion/update', views.viewUpdatePromotion, name="update-promotion"),
    path('promotion/list', views.viewGetPromotions, name="list-promotion"),

    # Reserves
    path('reserve/register', views.viewRegisterReserve, name="register-reserve"),
    path('reserve/update', views.viewUpdateReserve, name="update-reserve"),
    path('reserve/list', views.viewGetReserves, name="list-reserve"),

    # Room
    path('room/register', views.viewRegisterRoom, name="register-room"),
    path('room/update', views.viewUpdateRoom, name="update-room"),
    path('room/list', views.viewGetRooms, name="list-room"),

    # testimonial
    path('testimonial/register', views.viewRegisterTestimonial, name="register-testimonial"),
    path('testimonial/update', views.viewUpdateTestimonial, name="update-testimonial"),
    path('testimonial/list', views.viewGetTestimonials, name="list-testimonial"),

    # dashboard 
    path('dashboard/indicators', views.viewGetDashboardIndicators, name="dashboard-indicators"),
]