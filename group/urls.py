from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("create", views.create_group, name="create_group"),
]
