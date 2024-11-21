from django.contrib import admin
from .models import Notification, Profile, Event, Ticket, Venue, BankAccount, EventDeletionRequest, Review, Interest, ReviewLikeDislike
# Register your models here.

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Venue)
admin.site.register(BankAccount)
admin.site.register(EventDeletionRequest)
admin.site.register(Notification)
admin.site.register(Review)
admin.site.register(Interest)
admin.site.register(ReviewLikeDislike)
