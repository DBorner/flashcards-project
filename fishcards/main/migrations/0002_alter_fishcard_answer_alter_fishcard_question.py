# Generated by Django 5.0.1 on 2024-01-24 12:47

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fishcard',
            name='answer',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='fishcard',
            name='question',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
