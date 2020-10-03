from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListings(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    active_status = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    image_url = models.URLField(max_length=200, blank=True, default="")
    category = models.CharField(
        max_length=50, blank=True, default="No Category Listed")
    creation_time = models.DateTimeField(auto_now_add=True, blank=True)


class Bids(models.Model):
    listing_id = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name="bid")
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
    creation_date = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    listing_id = models.ForeignKey(
        AuctionListings, blank=True, on_delete=models.CASCADE, related_name="comments")
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)


class Watchlists(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlists")
    item = models.ManyToManyField(
        AuctionListings, blank=True, related_name="watchlists")
