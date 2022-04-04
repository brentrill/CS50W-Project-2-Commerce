from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max


from .models import User, Categories, Listings, Bids, Comments
from . import forms


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Listings.objects.filter(closed=False),
        "title": 'Active Listings'
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
    else:
        return render(request, "auctions/register.html")


def listing(request, id):
    listing_id = Listings.objects.get(id=id)

    info = {}
    info['listing'] = listing_id
    info['bids'] = forms.BidForm()
    info['comments'] = forms.CommentForm()
    info['buyer'] = False
    if listing_id.is_closed():
        info['closed'] = True

    return render(request, "auctions/listing.html", info)


@login_required
def create(request):
    form = forms.ListingForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        listing = form.save(commit=False)
        listing.seller = request.user
        listing.save()

        return HttpResponseRedirect(reverse('listing', kwargs={'id': listing.id}))
    else:
        return render(request, "auctions/create.html", {
            "form": form
        })


def watch(request, id):
    if request.method == "POST":
        listing = Listings.objects.get(id=id)
        watchlist = request.user.watchers
        if listing in watchlist.all():
            watchlist.remove(listing)
        else:
            watchlist.add(listing)

    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))


def bid(request, id):
    form = forms.BidForm(request.POST or None)
    error = None

    if form.is_valid():
        listing = Listings.objects.get(id=id)
        bid = form.save(commit=False)
        highest = Bids.objects.filter(listing=listing).aggregate(Max('amount')).get('amount__max')
        if not highest:
            highest = 0

        if (bid.amount >= listing.starting_bid) and (bid.amount > highest):
            bid.listing, bid.bidder = listing, request.user
            bid.save()
        else:
            error = 'Invalid Bid.'
            messages.error(request, error)

    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))


def close(request, id):
    listing = Listings.objects.get(id=id)
    listing.closed = True
    listing.save()

    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))


def comment(request, id):
    form = forms.CommentForm(request.POST or None)

    if form.is_valid():
        comment_db = form.save(commit=False)
        comment_db.user = request.user
        comment_db.listing = Listings.objects.get(id=id)
        comment_db.save()

    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "auctions": Listings.objects.filter(watchlist=request.user)
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all()
    })


def category(request, name):
    category_name = Categories.objects.get(category=name)

    return render(request, "auctions/index.html", {
        "auctions": Listings.objects.filter(
                        category=category_name,
                        closed=False
                        ),
        "title": category_name
    })
