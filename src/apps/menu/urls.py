from django.contrib import admin
from django.urls import path

from apps.menu import views


urlpatterns = [
    path('', views.index, name='menu'),
    path('<slug:menu_slug>/', views.index, name='select_menu'),
]
