from django.contrib import admin
from main.models import FishCardSet, FishCard, UserTry, UserTryCard

admin.site.site_header = "Fishcards Admin"
admin.site.site_title = "Fishcards Admin Portal"
admin.site.index_title = "Welcome to Fishcards Researcher Portal"


class FishCardInline(admin.TabularInline):
    model = FishCard
    extra = 1


@admin.register(FishCardSet)
class FishCardSetAdmin(admin.ModelAdmin):
    inlines = [FishCardInline]
    search_fields = ["name"]
    list_display = ("name", "description", "created_at", "updated_at")
    list_filter = ["created_at", "updated_at"]


@admin.register(FishCard)
class FishCardAdmin(admin.ModelAdmin):
    search_fields = ["question"]
    list_display = ("question", "answer")
    list_filter = ["fishcardset"]


class UserTryCardInline(admin.TabularInline):
    model = UserTryCard
    extra = 1


@admin.register(UserTry)
class UserTryAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    list_display = ("user", "fishcardset", "created_at", "updated_at")
    list_filter = ["created_at", "updated_at"]
    inlines = [UserTryCardInline]
