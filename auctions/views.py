from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bidding, Comments, Categories


def index(request):
    allObjects = Listing.objects.all()
    activeObjects = Listing.objects.all().filter(active = True)
  
    return render(request, "auctions/index.html", {
        "allObjects": activeObjects
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


def addListing(request):
    categories = Categories.objects.all()

    if request.method == "POST":
        #get all the info from Form and save it in variables
        title = request.POST["title"]
        description = request.POST["desc"]
        imageUrl = request.POST["imageUrl"]
        startingBid = request.POST["startingBid"]
        currentUser = request.user
        getCategory = request.POST["category"]
        currentCategory = Categories.objects.get(category = getCategory)
        #create object for starting bid
        add2 = Bidding(newBid = startingBid)
        add2.save()
        #add listing
        add = Listing(title=title, description=description, imagelink=imageUrl, creator = currentUser, startbid = add2, category = currentCategory)
        add.save()
        
        


    
        return HttpResponseRedirect(reverse("addListing"))

    else:
        if request.user.is_authenticated:
    
            return render(request, "auctions/createListing.html", {

            "categories": categories
              })
        else:
            return HttpResponseRedirect(reverse("login"))


def listingPage(request, listingID):
    #get current listing
    currentListing = Listing.objects.get(pk=listingID)
    #get current user
    currentUser = request.user
    #get current watchlist query, as it's manytomanyfield
    currentWatchlist = currentListing.watchlist.all()
    #check if current user is in that query
    isUserInList = currentUser in currentWatchlist

    #find comments for this listing
    currentComments = Comments.objects.filter(listing = currentListing)

    #toggle active status
    if  request.method == "POST":
        if currentListing.active:
            currentListing.active = False
            currentListing.save()
            
            
            
        else:
            currentListing.active = True
            currentListing.save()
            


        return render(request, "auctions/listingPage.html", {
        "listingID": listingID,
        "currentListing": currentListing,
        "isUserInList": isUserInList,
        "currentUser": currentUser,
        "currentComments": currentComments
        
    })
    return render(request, "auctions/listingPage.html", {
        "listingID": listingID,
        "currentListing": currentListing,
        "isUserInList": isUserInList,
        "currentUser": currentUser,
       "currentComments": currentComments

    })

    

   

    

def addToWatchlist(request, currListing):
    getCurrentListing = Listing.objects.get(pk=currListing)
    currentUser = request.user
    getCurrentListing.watchlist.add(currentUser)

    return HttpResponseRedirect(reverse('listingPage', args=[currListing,]))

    

def removeWatchlist(request, currListing):
    getCurrentListing = Listing.objects.get(pk=currListing)
    currentUser = request.user
    getCurrentListing.watchlist.remove(currentUser)

    return HttpResponseRedirect(reverse('listingPage', args=[currListing,]))

def watchlist(request):
    if request.user.is_authenticated:
        currentUser = request.user
        allObjects = currentUser.watchList.all()  

        return render(request, "auctions/watchList.html", {
            "allObjects": allObjects
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def bidding(request, currListing):
    #get bid info
    requestBid = request.POST["placeBid"]
    currentUser = request.user
    #create instance for that bid model
    bid = Bidding(newBid=int(requestBid), user=currentUser)
    bid.save()
    #get current listing
    getCurrentListing = Listing.objects.get(pk=currListing)
    #check current listing's watchlist situation
    currentWatchlist = getCurrentListing.watchlist.all()
    isUserInList = currentUser in currentWatchlist
    
    #if new bid is higher than older, update it
    if int(requestBid) > getCurrentListing.startbid.newBid:
        getCurrentListing.startbid = bid
        getCurrentListing.save()
    
        return HttpResponseRedirect(reverse('listingPage', args=[currListing,]))
    else:
        return render(request,"auctions/listingPage.html", {
        "listingID": currListing,
        "currentListing": getCurrentListing,
        "isUserInList": isUserInList,
        "currentUser": currentUser,
        "errorMessage": "New bid should be higher than the current one!"
        })

def addComment(request, currListing):
    currentUser = request.user
    requestComm = request.POST["comm"]
    getCurrentListing = Listing.objects.get(pk=currListing)
    comments = Comments(author = currentUser,
                listing = getCurrentListing,
                comment = requestComm)
    comments.save()

    return HttpResponseRedirect(reverse('listingPage', args=[currListing,]))



def categories(request):
    allCategories = Categories.objects.all()
    
    return render(request, "auctions/categories.html", {
        "allCategories" : allCategories
    })

def categoryPage(request, currCategory):
    getCurrentCategoryName = Categories.objects.get(pk=currCategory)
    allObjects = Listing.objects.filter(category = currCategory, active = True)
    
    
    return render(request, "auctions/categoryPage.html",       {
        "allObjects" : allObjects,
        "getCurrentCategoryName": getCurrentCategoryName
    })

def myListing(request):
    myObjects = Listing.objects.filter(creator = request.user)

    return render(request, "auctions/mylisting.html",{
        "allObjects": myObjects
    })
