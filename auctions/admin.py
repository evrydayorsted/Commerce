from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Listing)
admin.site.register(Wishlist)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)

