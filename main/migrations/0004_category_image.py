# Generated by Django 4.1.2 on 2022-10-13 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_category_name_en_category_name_ru_category_slug_ru'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='no_image.jpg', upload_to='category_images'),
        ),
    ]
