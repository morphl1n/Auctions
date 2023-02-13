from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#bids
class Bidding(models.Model):
    newBid = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True, related_name="userbid", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.newBid}"

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


#listing, must have: title, text-based description, starting bid, url for image
class Listing(models.Model):
    title = models.CharField(max_length=64)
    active = models.BooleanField(default = True)
    description = models.TextField()
    imagelink = models.URLField()
    startbid = models.ForeignKey(Bidding, blank=True, null=True, related_name="bidding", on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchList")
    creator = models.ForeignKey(User,  blank=True, null=True, related_name="creator", on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, blank=True, null=True, related_name="categories", on_delete=models.CASCADE)
   

    def __str__(self):
        return f"{self.title}, active status: {self.active}, {self.category}, {self.description}, {self.startbid}, {self.imagelink}"



#comments on auction listings
class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,blank=True, null=True, related_name="listing" )
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="author" )
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment}, {self.author}"

