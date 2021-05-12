from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Wishlist, Bid, Comment

categories= ["Fashion", "Toys", "Electronics", "Home"]

def index(request):
    p = request.user
    if request.user.is_authenticated:
        x = p.wishlist_set.all()
    else:
        x = None
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "wishlist": x
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

def create(request):
    if request.method == "POST":
        f = Listing(
            title=request.POST["title"],
            description=request.POST["description"],
            image_url=request.POST["image_url"],
            category=request.POST["category"],
            highest_bid=int(request.POST["bid"]),
            poster=request.user
            )
        f.save()
        g = Bid(
            thingy=f,
            bidder=request.user,
            value=request.POST["bid"]
        )
        g.save()
        f.bid = g
        f.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "categories": categories
    })

def show_item(request, item):
    try:
        thing = Listing.objects.get(title=item)
    
        error = False
        k = thing.bids.get(value=thing.highest_bid)
        
        if request.method == "POST":
            
            if request.POST["button"] == "add":
                try:
                    f = Wishlist.objects.get(
                        listing=Listing.objects.get(title=item)
                        )
                except Wishlist.DoesNotExist:
                    f = Wishlist(
                        listing=Listing.objects.get(title=item)
                    )
                    f.save()
                f.users.add(request.user)
                f.save()
            elif request.POST["button"] == "remove":
                try:
                    f = Wishlist.objects.get(
                        listing=Listing.objects.get(title=item)
                        )
                except Wishlist.DoesNotExist:
                    f = Wishlist(
                        listing=Listing.objects.get(title=item)
                    )
                    f.save()
                f.users.remove(request.user)
                f.save()
            elif request.POST["button"] == "bid":
                if int(request.POST["bid_value"]) > thing.highest_bid:
                    g = Bid(thingy=thing, bidder=request.user, value=request.POST["bid_value"])
                    g.save()
                    thing.highest_bid = int(request.POST["bid_value"])
                    thing.save()
                else:
                    error = True
            elif request.POST["button"] == "close":
                thing.active = False
                thing.save()
                k = thing.bids.get(value=thing.highest_bid)
            elif request.POST["button"] == "comment":
                h = Comment(
                    thingy=thing,
                    commenter=request.user,
                    value=request.POST["comment_text"]
                )
                h.save()
        try:
            l = Comment.objects.filter(thingy=thing)
        except Comment.DoesNotExist:
            l = None
        return render(request, "auctions/item.html", {
            "item": item,
            "title": thing.title,
            "description": thing.description,
            "bid": thing.highest_bid,
            "image_url": thing.image_url,
            "error": error,
            "poster": thing.poster,
            "active": thing.active,
            "winner": k,
            "all_comments": l
        })
    except Listing.DoesNotExist:
        return index(request)

def active(request):
    return render(request, "auctions/active.html", {
        "listings": Listing.objects.all()
    })
def wishlist(request):
    return render(request, "auctions/wishlist.html", {
        "wishlist": Wishlist.objects.filter(users=request.user)
    })

def category(request):
    return render(request, "auctions/category.html", {
        "categories": categories
    })

def catlist(request, cat):
    stuff = Listing.objects.filter(category=cat)
    return render(request, "auctions/catlist.html", {
        "stuff": stuff,
        "cat": cat
    })
