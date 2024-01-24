import os
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
from main.utils import set_file_name, CustomRichTextUploadingField


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
