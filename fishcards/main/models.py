import os
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
from main.utils import set_file_name, CustomRichTextUploadingField
from django.contrib.auth.models import User


class FishCardSet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=set_file_name, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class FishCard(models.Model):
    fishcardset = models.ForeignKey(FishCardSet, on_delete=models.SET_NULL, null=True)
    question = CustomRichTextUploadingField()
    answer = CustomRichTextUploadingField()

    def __str__(self) -> str:
        if len(self.question) > 33:
            return self.question[3:33] + "..."
        if len(self.question) == 0:
            return "No question"
        return self.question[3:]


class UserTry(models.Model):
    fishcardset = models.ForeignKey(FishCardSet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.user} - {self.fishcardset}"
    
    def get_correct_cards(self):
        return UserTryCard.objects.filter(usertry=self, status=UserTryCard.Status.CORRECT)
    
    def get_semi_correct_cards(self):
        return UserTryCard.objects.filter(usertry=self, status=UserTryCard.Status.SEMI_CORRECT)
    
    def get_wrong_cards(self):
        return UserTryCard.objects.filter(usertry=self, status=UserTryCard.Status.WRONG)
    
    def get_not_answered_cards(self):
        return UserTryCard.objects.filter(usertry=self, status=UserTryCard.Status.NOT_ANSWERED)
    
    def get_all_cards(self):
        return UserTryCard.objects.filter(usertry=self)
    
    def get_all_unanswered_cards_ids(self):
        return [card.id for card in self.get_not_answered_cards().order_by("?")]
    
    @property
    def is_finished(self):
        return len(self.get_not_answered_cards()) == 0
    
    @property
    def number_of_cards(self):
        return len(self.get_all_cards())
    
    @property
    def completed_percentage(self):
        return int((self.number_of_cards - len(self.get_not_answered_cards())) / self.number_of_cards * 100)

class UserTryCard(models.Model):
    class Status(models.TextChoices):
        NOT_ANSWERED = "not_answered", "Not Answered"
        CORRECT = "correct", "Correct"
        SEMI_CORRECT = "semi_correct", "Semi Correct"
        WRONG = "wrong", "Wrong"

    usertry = models.ForeignKey(UserTry, on_delete=models.CASCADE)
    fishcard = models.ForeignKey(FishCard, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NOT_ANSWERED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
