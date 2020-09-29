from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Bids(models.Model):
    listing = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name="bids")
    author = models.ForeignKey(User)
    amount = models.IntegerField()


class Comments(models.Model):
    listing = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)


class AuctionListings(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    image_url = models.URLField(max_length=200, blank=True, default="")
    category = models.CharField(
        max_length=50, blank=True, default="No Category Listed")
    creation_time = models.DateTimeField(auto_now_add=True, blank=True)
    bid = models.ForeignKey(
        Bids, on_delete=models.CASCADE, related_name="listing")
    comments = models.ForeignKey(
        Comments, on_delete=models.CASCADE, related_name="listing")
