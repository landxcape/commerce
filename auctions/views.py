from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListings, Bids
from .forms import CreateListingForm, PlaceBidForm


def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": AuctionListings.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")


def categories(request):
    return render(request, "auctions/categories.html")


def watchlist(request):
    return render(request, "auctions/watchlist.html")


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        try:
            auction_listing = AuctionListings(
                user_id=request.user,
                title=title,
                description=description,
                image_url=image_url,
                category=category
            )
            bid = Bids(
                listing_id=auction_listing,
                user_id=request.user,
                amount=bid
            )
            auction_listing.save()
            bid.save()
            message = "Saved..."
        except IntegrityError:
            if auction_listing.id:
                auction_listing.delete()
            if bid.id:
                bid.delete()
            message = "Error. Fill the form correctly."
        return render(request, "auctions/create_listing.html", {
            "message": message,
            "create_listing_form": CreateListingForm()
        })
    return render(request, "auctions/create_listing.html", {
        "create_listing_form": CreateListingForm()
    })


@login_required(login_url="login")
def listing(request, _listing_id):
    return render(request, "auctions/listing.html", {
        "listing": AuctionListings.objects.get(id=_listing_id),
        "place_bid_form": PlaceBidForm()
    })


@login_required(login_url="login")
def place_bid(request, _listing_id):
    if request.method == "POST":
        pass
    return render(request, "auctions/index.html", {
        "message": "Select a product first to bid...",
        "active_listings": AuctionListings.objects.all(),
    })
