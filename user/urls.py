from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("search", views.search_usernames, name="search"),
    path("all", views.get_users, name="get_users"),
]
