from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListings(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    bid = models.IntegerField()
    image_url = models.URLField(max_length=200, blank=True, default="")
    category = models.CharField(
        max_length=50, blank=True, default="No Category Listed")
    creation_time = models.DateTimeField(auto_now_add=True, blank=True)


class Bids(models.Model):
    pass


class Comments(models.Model):
    pass
