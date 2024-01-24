from django.contrib import admin
from main.models import FishCardSet, FishCard

admin.site.site_header = "Fishcards Admin"
admin.site.site_title = "Fishcards Admin Portal"
admin.site.index_title = "Welcome to Fishcards Researcher Portal"
admin.site.register(FishCardSet)
admin.site.register(FishCard)
