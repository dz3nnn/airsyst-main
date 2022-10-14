from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from .utils import lat_to_cyr_slugify
from tinymce import models as tinymce_models
from django.utils.translation import gettext as _
from .utils import uuid_generator


SERVICE_CHOICES = (
    ('MAINTENANCE', _('Обслуживание')),
    ('REPAIR', _('Сервис')),
    ('SELL', _('Продажи')),
)


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='category_images', default='no_image.jpg')
    slug = models.SlugField(editable=False, unique=True)
    slug_ru = models.SlugField(editable=False, blank=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.slug_ru = lat_to_cyr_slugify(self.name_ru)
        super(Category, self).save(*args, **kwargs)


class Country(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    flag = models.ImageField(upload_to='country_flags/',
                             verbose_name='Флаг', null=True, blank=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Brand(models.Model):
    """ Бренд """
    name = models.CharField(
        max_length=200, verbose_name='Название')
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='Страна', null=True, blank=True)
    logo = models.FileField(upload_to='brand_logos/',
                            verbose_name='Логотип', null=True, blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название')
    logo = models.ImageField(upload_to='company_logos/',
                             verbose_name='Логотип', null=True, blank=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name


class Project(models.Model):
    project_type = models.CharField(
        max_length=20, choices=SERVICE_CHOICES, verbose_name='Вид работ', null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name='Бренд')
    date = models.DateField(verbose_name='Дата')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name='Организация')
    title = models.CharField(
        max_length=250, verbose_name='Заголовок')
    description = tinymce_models.HTMLField(
        verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return u"%s - %s (№%s)" % (self.get_project_type_display(), self.company.name, self.pk)


class Project_Image(models.Model):
    """Галерея проекта """
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='Проект')
    image = models.ImageField(upload_to='project_images/',
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение проекта'
        verbose_name_plural = 'Изображения проекта'

    def __str__(self):
        return u"изображение (id:%s)" % (self.pk)


class Information(models.Model):
    ru = tinymce_models.HTMLField(
        verbose_name='ru site', null=True, blank=True)
    by = tinymce_models.HTMLField(
        verbose_name='by site', null=True, blank=True)
    ie = tinymce_models.HTMLField(
        verbose_name='ie site', null=True, blank=True)
    eu = tinymce_models.HTMLField(
        verbose_name='eu site', null=True, blank=True)
    description = models.CharField(
        max_length=250, verbose_name='Описание', null=True, blank=True)
    uid = models.TextField(primary_key=True, default=uuid_generator)

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информация'

    def __str__(self):
        return u"%s (uid:%s)" % (self.description, self.uid)
