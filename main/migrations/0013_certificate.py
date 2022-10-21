# Generated by Django 4.1.2 on 2022-10-20 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_equipment_image_option_optionrelation_optionvalue_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Certificate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="certificate_images/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "equipment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="main.equipment_item",
                        verbose_name="Оборудование",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сертификат",
                "verbose_name_plural": "Сертификаты",
            },
        ),
    ]