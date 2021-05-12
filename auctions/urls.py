from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin", admin.site.urls, name="admin"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("active", views.active, name="active"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("category", views.category, name="category"),
    path("catlist/<str:cat>", views.catlist, name="catlist"),
    path("<str:item>", views.show_item, name="item")
]
