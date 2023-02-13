from django.contrib import admin
from .models import Listing, Bidding, User, Comments, Categories

# Register your models here.

admin.site.register(Listing)
admin.site.register(Bidding)
admin.site.register(User)
admin.site.register(Comments)  
admin.site.register(Categories)