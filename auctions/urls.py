from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addListing, name="addListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listingID>", views.listingPage, name="listingPage"),
    path("add/<int:currListing>", views.addToWatchlist, name="addToWatchlist"),
    path("remove/<int:currListing>", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bidding/<int:currListing>", views.bidding, name="bidding"),
    path("addcomment/<int:currListing>", views.addComment, name="addcomment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:currCategory>", views.categoryPage, name="categoryPage"),
    path("mylisting", views.myListing, name="myListing")
   

]
