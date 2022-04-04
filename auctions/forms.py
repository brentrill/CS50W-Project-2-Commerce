from django.forms import ModelForm
from .models import Listings, Bids, Comments

class ListingForm(ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'starting_bid', 'image', 'image_link', 'category']


class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']