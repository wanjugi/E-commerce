from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import User, Category,Listing, Comment, Bid


 


def index(request):
    activeListings = Listing.objects.filter(active=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activeListings,
        "categories":allCategories,
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

def Categories(request):
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "categories":allCategories,
    })
    

def Create_Listing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/CreateList.html",{
            "categories":allCategories
        })
        
    else:
        title = request.POST['title']
        description = request.POST['description']
        imageUrl = request.POST['imageUrl']
        price = request.POST['price']
        category = request.POST['category']
        
        currentUser= request.user
        
        categoryInfo= Category.objects.get(categoryName=category)
        bid= Bid(bid=float(price),user=currentUser)
        bid.save()
        newListing = Listing (
            title= title,
            description=description,
            imageUrl=imageUrl,
            price=bid,
            category = categoryInfo,
            owner=currentUser,
        )
        
        newListing.save()
        return HttpResponseRedirect(reverse(index))
    
        
def Watchlist(request):
        currentUser= request.user
        listings = currentUser.watchlistListing.all()
        return render(request, "auctions/watchlist.html",{
            "listings":listings,
        })
    
    
def showCategory(request):
    if request.method == 'POST':
       getCategoryFromform = request.POST['category']
       category = Category.objects.get(categoryName=getCategoryFromform)
       activeListings = Listing.objects.filter (active=True, category= category)
       allCategories = Category.objects.all()
       return render(request, "auctions/index.html",{
          "listings":activeListings,
          "categories":allCategories,
        })
       
def listing(request, id):
    listingInfo = Listing.objects.get(pk=id)
    ListingInWatchlist = listingInfo.watchlist.filter(pk=request.user.id)
    allComments = Comment.objects.filter(listing=listingInfo)
    isOwner = request.user.username == listingInfo.owner.username
    return render(request, 'auctions/listing.html', {
        'listing': listingInfo,
        'ListingInWatchlist': ListingInWatchlist,
        "allComments":allComments,
        "isOwner":isOwner,
    })
    
       
def removeWatchlist(request, id):
    currentUser = request.user
    listingInfo = Listing.objects.get(pk=id)
    listingInfo.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))

def addWatchlist(request, id):
    print("Hello world!")
    currentUser = request.user
    listingInfo = Listing.objects.get(pk=id)
    listingInfo.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))


def addComment(request, id):
    currentUser= request.user
    listingInfo = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    
    newComment = Comment(
        author= currentUser,
        listing= listingInfo,
        message= message
    )
    newComment.save()
    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
 
def closeAuction(request, id):
    listingInfo = Listing.objects.get(pk=id)
    listingInfo.active = False
    listingInfo.save()
    ListingInWatchlist = listingInfo.watchlist.filter(pk=request.user.id)
    allComments = Comment.objects.filter(listing=listingInfo)
    isOwner = request.user.username == listingInfo.owner.username
    return render(request, 'auctions/listing.html', {
        'listing': listingInfo,
        'ListingInWatchlist': ListingInWatchlist,
        "allComments":allComments,
        "isOwner":isOwner,
        "update":True,
        "message": "Congratulations You Have Closed The Auction."
    })     
            
def addBid(request, id):
    newBid = request.POST.get('newBid')
    listingInfo = Listing.objects.get(pk=id)
    ListingInWatchlist = listingInfo.watchlist.filter(pk=request.user.id)
    allComments = Comment.objects.filter(listing=listingInfo)
    isOwner = request.user.username ==listingInfo.owner.username
    if newBid is not None and newBid.isdigit() and int(newBid) > listingInfo.price.bid:
        if not Bid.objects.filter(bid=newBid).exists():
            updateBid = Bid(user=request.user, bid=newBid)
            updateBid.save()
            listingInfo.price = updateBid
            listingInfo.save()
            return render(request, "auctions/listing.html",{
                "listing": listingInfo,
                "message": "BID UPDATE WAS SUCCESSFULL",
                "update": True,
                'ListingInWatchlist': ListingInWatchlist,
                "allComments":allComments,
                "isOwner":isOwner,
                
            })
        else:
            return render(request, "auctions/listing.html",{
                "listing": listingInfo,
                "message": "BID UPDATE FAILED",
                "update": False,
                'ListingInWatchlist': ListingInWatchlist,
                "allComments":allComments,
                "isOwner":isOwner,
                
            })
    else:
        return render(request, "auctions/listing.html",{
            "listing": listingInfo,
            "message": "BID UPDATE FAILED",
            "update": False,
            'ListingInWatchlist': ListingInWatchlist,
            "allComments":allComments,
            "isOwner":isOwner,
            
        })
  
    
    

        
  