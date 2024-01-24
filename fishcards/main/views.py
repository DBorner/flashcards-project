from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from .models import *
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


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
        context["title"] = "Fish Cards"
        return context


@login_required
def start_try(request, fishcardset_id):
    fishcardset = FishCardSet.objects.get(id=fishcardset_id)
    if FishCard.objects.filter(fishcardset=fishcardset).count() == 0:
        messages.error(request, "This set has no cards")
        return redirect("home")
    user_try = UserTry.objects.create(fishcardset=fishcardset, user=request.user)
    fishcards = FishCard.objects.filter(fishcardset=fishcardset).order_by("?")
    user_try_cards = []
    for fishcard in fishcards:
        user_try_cards.append(
            UserTryCard.objects.create(usertry=user_try, fishcard=fishcard).id
        )
    request.session["user_try_cards"] = user_try_cards
    return redirect("try_card", user_try_cards[0])


class TryCardView(TemplateView):
    template_name = "try_card.html"

    def get(self, request, try_card_id):
        try_card = get_object_or_404(UserTryCard, id=try_card_id)
        user_try = try_card.usertry
        if try_card.usertry.user != request.user:
            messages.error(request, "You are not allowed to see this card")
            return redirect("home")
        correct_cards = len(user_try.get_correct_cards())
        semi_correct_cards = len(user_try.get_semi_correct_cards())
        wrong_cards = len(user_try.get_wrong_cards())
        cards_total = len(user_try.get_all_cards())
        cards_done = correct_cards + semi_correct_cards + wrong_cards
        done_percentage = int(cards_done / cards_total * 100)
        context = {
            "try_card": try_card,
            "cards_total": cards_total,
            "cards_done": cards_done,
            "done_percentage": done_percentage,
            "card_id": try_card.id,
            "correct_cards": correct_cards,
            "semi_correct_cards": semi_correct_cards,
            "wrong_cards": wrong_cards,
        }
        print(context)
        return render(request, self.template_name, context)

    def post(self, request, try_card_id):
        try_card = get_object_or_404(UserTryCard, id=try_card_id)
        if try_card.usertry.user != request.user:
            messages.error(request, "You are not allowed to see this card")
            return redirect("home")
        if "answer" in request.POST:
            answer = request.POST["answer"]
            if answer == "correct":
                try_card.status = UserTryCard.Status.CORRECT
                try_card.save()
                messages.success(request, "Correct")
            elif answer == "semi-correct":
                try_card.status = UserTryCard.Status.SEMI_CORRECT
                try_card.save()
                messages.success(request, "Semi Correct")
            elif answer == "wrong":
                try_card.status = UserTryCard.Status.WRONG
                try_card.save()
                messages.success(request, "Wrong")
        else:
            messages.error(request, "Something went wrong")
        if "user_try_cards" in request.session:
            user_try_cards = request.session["user_try_cards"]
            if try_card.id in user_try_cards:
                user_try_cards.remove(try_card.id)
                request.session["user_try_cards"] = user_try_cards
                if len(user_try_cards) > 0:
                    return redirect("try_card", user_try_cards[0])
                else:
                    return redirect("try_detail", try_card.usertry.id)
        return redirect("try_detail", try_card.usertry.id)


class UserTryDetailView(TemplateView):
    template_name = "try_detail.html"

    def get(self, request, user_try_id):
        user_try = get_object_or_404(UserTry, id=user_try_id)
        if user_try.user != request.user:
            messages.error(request, "You are not allowed to see this card")
            return redirect("home")
        correct_cards = len(user_try.get_correct_cards())
        semi_correct_cards = len(user_try.get_semi_correct_cards())
        wrong_cards = len(user_try.get_wrong_cards())

        cards_done = correct_cards + semi_correct_cards + wrong_cards
        all_questions = user_try.get_all_cards()
        cards_total = len(all_questions)
        done_percentage = int(cards_done / cards_total * 100)
        if cards_total == cards_done:
            is_finished = True
        else:
            is_finished = False
        context = {
            "user_try": user_try,
            "all_questions": all_questions,
            "cards_total": cards_total,
            "cards_done": cards_done,
            "done_percentage": done_percentage,
            "correct_cards": correct_cards,
            "semi_correct_cards": semi_correct_cards,
            "wrong_cards": wrong_cards,
            "is_finished": is_finished,
        }
        return render(request, self.template_name, context)

    def post(self, request, user_try_id):
        user_try = get_object_or_404(UserTry, id=user_try_id)
        if user_try.user != request.user:
            messages.error(request, "You are not allowed to see this card")
            return redirect("home")
        if "answer" in request.POST:
            answer = request.POST["answer"]
            new_user_try = UserTry.objects.create(
                fishcardset=user_try.fishcardset, user=request.user
            )
            new_try_cards = []
            new_try_cards.extend(user_try.get_wrong_cards())
            if answer == "correct" or answer == "semi-correct":
                new_try_cards.extend(user_try.get_semi_correct_cards())
            if answer == "correct":
                new_try_cards.extend(user_try.get_correct_cards())
            if len(new_try_cards) == 0:
                messages.error(request, "Something went wrong (no cards to retry)")
                UserTry.objects.filter(id=new_user_try.id).delete()
                return redirect("try_detail", user_try.id)
            else:
                for new_try_card in new_try_cards:
                    UserTryCard.objects.create(
                        usertry=new_user_try, fishcard=new_try_card.fishcard
                    )
            request.session["user_try_cards"] = new_user_try.get_all_unanswered_cards_ids()
            return redirect("try_card", request.session["user_try_cards"][0])
        else:
            messages.error(request, "Something went wrong")
            return redirect("try_detail", user_try.id)

def restore_try(request, user_try_id):
    user_try = get_object_or_404(UserTry, id=user_try_id)
    if user_try.user != request.user:
        messages.error(request, "You are not allowed to see this card")
        return redirect("home")
    if user_try.is_finished():
        messages.error(request, "You can't restore a finished try")
        return redirect("home")
    request.session["user_try_cards"] = user_try.get_all_unanswered_cards_ids()
    return redirect("try_card", request.session["user_try_cards"][0])
