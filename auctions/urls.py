from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:_listing_id>", views.listing, name="listing"),
    path("place_bid/<str:_listing_id>", views.place_bid, name="place_bid"),
    path("watchlist_add/<str:_listing_id>",
         views.watchlist_add, name="watchlist_add"),
    path("close_listing/<str:_listing_id>",
         views.close_listing, name="close_listing"),
    path("delete_listing/<str:_listing_id>",
         views.delete_listing, name="delete_listing")
]
