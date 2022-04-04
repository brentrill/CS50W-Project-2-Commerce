from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("listing/<str:id>/watch", views.watch, name="watch"),
    path("listing/<str:id>/bid", views.bid, name="bid"),
    path("listing/<str:id>/close", views.close, name="close"),
    path("listing/<str:id>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watching"),
    path("categories", views.categories, name="categories_list"),
    path("categories/<str:name>", views.category, name="category"),
]
