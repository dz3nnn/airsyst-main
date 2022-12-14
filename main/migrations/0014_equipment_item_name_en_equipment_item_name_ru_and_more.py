# Generated by Django 4.1.2 on 2022-10-21 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0013_certificate"),
    ]

    operations = [
        migrations.AddField(
            model_name="equipment_item",
            name="name_en",
            field=models.CharField(max_length=100, null=True, verbose_name="Название"),
        ),
        migrations.AddField(
            model_name="equipment_item",
            name="name_ru",
            field=models.CharField(max_length=100, null=True, verbose_name="Название"),
        ),
        migrations.AddField(
            model_name="equipment_item",
            name="slug",
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name="equipment_item",
            name="slug_ru",
            field=models.SlugField(blank=True, editable=False),
        ),
    ]
