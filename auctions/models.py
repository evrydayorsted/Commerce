from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    highest_bid = models.IntegerField()
    image_url = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", default='')
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.title

class Wishlist(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, related_name="wishlist_set")

    def __str__(self):
        return self.listing.title


class Bid(models.Model):
    thingy = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default='')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", default='')
    value = models.IntegerField(default='')

    def __str__(self):
        return str(self.value)

class Comment(models.Model):
    thingy = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default='')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default='')
    value = models.TextField(default=None)

    def __str__(self):
        return self.value
