from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    seller = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(
                    max_digits=8,
                    decimal_places=2,
                    validators=[MinValueValidator(0)])
    image = models.ImageField(
                    upload_to='images/',
                    null=True,
                    blank=True)
    image_link = models.TextField(
                    null=True,
                    blank=True)
    category = models.ForeignKey(
                    Categories,
                    null=True,
                    blank=True,
                    on_delete=models.SET_NULL)
    watchlist = models.ManyToManyField(
                    User,
                    blank=True,
                    related_name="watchers")
    closed = models.BooleanField(default=False)

    def is_closed(self):
        return self.closed

    def __str__(self):
        return f"Listing {self.id}: {self.seller.username}, {self.title}"

class Bids(models.Model):
    bidder = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name="bidder")
    amount = models.DecimalField(
                    max_digits=8,
                    decimal_places=2)
    listing = models.ForeignKey(
                    Listings,
                    on_delete=models.CASCADE,
                    related_name="bid")

    def __str__(self):
        return f"Bid {self.id}: {self.bidder.username} {self.amount} {self.listing.title}"

class Comments(models.Model):
    user = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name="commenter")
    content = models.TextField()
    listing = models.ForeignKey(
                    Listings,
                    on_delete=models.CASCADE,
                    related_name="commented")

    def __str__(self):
        return f"Comment {self.id}: {self.user.username} ({self.listing.title}) {self.content}"