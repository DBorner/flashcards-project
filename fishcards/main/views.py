from django.shortcuts import render
from django.views.generic import TemplateView

from .models import *


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fish_card_sets = {}
        for fish_card_set in FishCardSet.objects.all():
            if FishCard.objects.filter(fishcardset=fish_card_set).exists():
                fish_card_sets[fish_card_set] = len(
                    FishCard.objects.filter(fishcardset=fish_card_set)
                )
        context["fish_card_sets"] = fish_card_sets
        print(context["fish_card_sets"])
        context["title"] = "Fish Cards"
        return context
