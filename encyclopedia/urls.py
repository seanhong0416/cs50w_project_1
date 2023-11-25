from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("random", views.random_page, name="random"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry"),
]
