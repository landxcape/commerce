from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListings, Bids, Comments, Watchlists
from .forms import CreateListingForm, CommentForm


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
    if request.method == "POST":
        category = request.POST["category"]
        category_list = AuctionListings.objects.filter(category=category)
        return render(request, "auctions/categories.html", {
            "category_list": category_list
        })
    categories = AuctionListings.objects.order_by().values_list("category").distinct()
    categories_list = map(lambda c: c[0], categories)
    return render(request, "auctions/categories.html", {
        "categories": categories_list
    })


@login_required(login_url="login")
def watchlist(request):
    my_watchlist = Watchlists.objects.filter(user_id=request.user)
    return render(request, "auctions/watchlist.html", {
        "my_watchlist": my_watchlist
    })


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
    get_listing = AuctionListings.objects.get(pk=_listing_id)
    max_bid = get_max_bid(get_listing, Bids)
    get_watchlist = Watchlists.objects.filter(
        user_id=request.user, item=get_listing.id).exists()
    return render(request, "auctions/listing.html", {
        "listing": get_listing,
        "max_bid": Bids.objects.filter(amount=max_bid).first(),
        "on_watchlist": get_watchlist,
        "comment_form": CommentForm(),
        "comments": Comments.objects.filter(listing_id=get_listing).order_by("-created_date")
    })


@login_required(login_url="login")
def place_bid(request, _listing_id):
    if request.method == "POST":
        _place_bid = request.POST["place_bid"]
        try:
            p_bid = Bids(
                user_id=request.user,
                listing_id=AuctionListings.objects.get(id=_listing_id),
                amount=_place_bid
            )
            p_bid.save()
            return HttpResponseRedirect(reverse("listing", args=[_listing_id]))
        except IntegrityError:
            return HttpResponseRedirect(reverse("listing", args=[_listing_id]))
    return render(request, "auctions/index.html", {
        "message": "Select a product first to bid...",
        "active_listings": AuctionListings.objects.all(),
    })


@login_required(login_url="login")
def watchlist_add(request, _listing_id):
    get_listing = get_object_or_404(AuctionListings, pk=_listing_id)
    get_watchlist = Watchlists.objects.filter(
        user_id=request.user, item=get_listing.id)
    if get_watchlist.exists():
        get_watchlist.delete()
        return HttpResponseRedirect(reverse("listing", args=[_listing_id]))
    user_watchlist, created = Watchlists.objects.get_or_create(
        user_id=request.user)
    user_watchlist.item.add(get_listing)
    return HttpResponseRedirect(reverse("listing", args=[_listing_id]))


@login_required(login_url="login")
def close_listing(request, _listing_id):
    get_listing = get_object_or_404(AuctionListings, pk=_listing_id)
    max_bid = get_max_bid(get_listing, Bids)
    get_watchlist = Watchlists.objects.filter(
        user_id=request.user, item=get_listing.id).exists()
    if Bids.objects.filter(amount=max_bid).first().user_id != request.user:
        get_listing.active_status = False
        get_listing.save()
        return HttpResponseRedirect(reverse("listing", args=[_listing_id]))
    return render(request, "auctions/listing.html", {
        "listing": get_listing,
        "max_bid": Bids.objects.filter(amount=max_bid).first(),
        "on_watchlist": get_watchlist,
        "close_listing_message": "No Highest bidder except the Auctioneer."
    })


@login_required(login_url="login")
def delete_listing(request, _listing_id):
    get_listing = get_object_or_404(AuctionListings, pk=_listing_id)

    if request.method == "POST":
        get_listing.delete()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/delete_listing.html", {
        "listing": get_listing
    })


@login_required(login_url="login")
def make_comment(request, _listing_id):
    get_listing = get_object_or_404(AuctionListings, pk=_listing_id)

    if request.method == "POST":
        comment = request.POST["comment"]
        try:
            m_comment = Comments(
                user_id=request.user,
                listing_id=AuctionListings.objects.get(id=_listing_id),
                text=comment
            )
            m_comment.save()
            return HttpResponseRedirect(reverse("listing", args=[_listing_id]))
        except IntegrityError:
            return HttpResponseRedirect(reverse("listing", args=[_listing_id]))
    return HttpResponseRedirect(reverse("index"))


def get_max_bid(listing, bid):
    return bid.objects.filter(listing_id=listing).aggregate(
        Max('amount')).get("amount__max")
