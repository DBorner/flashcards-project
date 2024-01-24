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
    fishcardset = models.ForeignKey(FishCardSet, on_delete=models.CASCADE)
    question = CustomRichTextUploadingField()
    answer = CustomRichTextUploadingField()

    def __str__(self) -> str:
        if len(self.question) > 30:
            return self.question[:30] + "..."
        return self.question


class UserTry(models.Model):
    fishcardset = models.ForeignKey(FishCardSet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
