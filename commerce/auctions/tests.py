from django.test import TestCase

# Create your tests here.
#def addBid(request, id):
    #newBid= request.POST['newBid']
    #listingInfo = Listing.objects.get(pk=id)
    #ListingInWatchlist = listingInfo.watchlist.filter(pk=request.user.id)
    #allComments = Comment.objects.filter(listing=listingInfo)
    #if int(newBid) > listingInfo.price.bid:
        #updateBid = Bid(user=request.user, bid=newBid)
       # updateBid.save()
       # listingInfo.price = updateBid
        #listingInfo.save()
        #return render(request, "auctions/listing.html",{
            #"listing": listing,
            #"message": "BID UPDATE WAS SUCCESSFULL",
            #"update": True,
           # 'ListingInWatchlist': ListingInWatchlist,
           # "allComments":allComments
        #})
    #else:
        #return render(request, "auctions/listing.html",{
           # "listing": listing,
            #"message": "BID UPDATE FAILED",
           # "update": False,
           # 'ListingInWatchlist': ListingInWatchlist,
          #  "allComments":allComments
       # })