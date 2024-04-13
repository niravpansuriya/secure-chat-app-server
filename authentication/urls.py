from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Path for user signup
    path("signup", views.signup, name="signup"),

    # Path for user login
    path("login", views.login, name="login"),

    # Path for user logout
    path("logout", views.logout, name="logout"),
]