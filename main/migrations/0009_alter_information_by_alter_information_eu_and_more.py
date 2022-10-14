# Generated by Django 4.1.2 on 2022-10-14 08:49

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_information_by_alter_information_eu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='by',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='by site'),
        ),
        migrations.AlterField(
            model_name='information',
            name='eu',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='eu site'),
        ),
        migrations.AlterField(
            model_name='information',
            name='ie',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='ie site'),
        ),
        migrations.AlterField(
            model_name='information',
            name='ru',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='ru site'),
        ),
    ]