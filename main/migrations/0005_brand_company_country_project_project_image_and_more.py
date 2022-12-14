# Generated by Django 4.1.2 on 2022-10-14 08:21

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('logo', models.FileField(blank=True, null=True, upload_to='brand_logos/', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos/', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('flag', models.ImageField(blank=True, null=True, upload_to='country_flags/', verbose_name='Флаг')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_type', models.CharField(blank=True, choices=[('MAINTENANCE', 'Обслуживание'), ('REPAIR', 'Сервис'), ('SELL', 'Продажи')], max_length=20, null=True, verbose_name='Вид работ')),
                ('date', models.DateField(verbose_name='Дата')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('description', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Описание')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.brand', verbose_name='Бренд')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.company', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='Project_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='project_images/', verbose_name='Изображение')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Изображение проекта',
                'verbose_name_plural': 'Изображения проекта',
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.country', verbose_name='Страна'),
        ),
    ]
