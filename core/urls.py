"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
"""
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
