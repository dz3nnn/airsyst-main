from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from .utils import lat_to_cyr_slugify


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
        verbose_name_plural = "categories"

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


def old_models():
    class Country(models.Model):
        """ Страна для брендов """
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
        """ Компании """
        name = models.CharField(
            max_length=200, verbose_name='Название')
        logo = models.ImageField(upload_to='company_logos/',
                                 verbose_name='Логотип', null=True, blank=True)

        class Meta:
            verbose_name = 'Компания'
            verbose_name_plural = 'Компании'

        def __str__(self):
            return self.name

    class ProductModel(models.Model):
        """ Модель продукта -> оборудование, запчасть """
        name = models.CharField(
            max_length=100, verbose_name='Название', null=True)
        article = models.CharField(
            max_length=8, verbose_name='Артикул', null=True, blank=True)
        price = models.DecimalField(
            max_digits=10, decimal_places=2, verbose_name='Цена поставщика (EUR)', null=True, blank=True)
        delivery_time = models.CharField(
            max_length=100, verbose_name='Срок доставки', null=True, blank=True)
        supply_time = models.CharField(
            max_length=100, verbose_name='Срок поставки', null=True, blank=True)
        warranty = models.CharField(
            max_length=100, verbose_name='Гарантия', null=True, blank=True)

        class Meta:
            abstract = True

    class ProductImageModel(models.Model):
        """ Изображение продукта """
        product = models.ForeignKey(
            ProductModel, on_delete=models.CASCADE, verbose_name='Товар')
        image = models.ImageField(upload_to='product_image/',
                                  verbose_name='Изображение')

        class Meta:
            verbose_name = 'Изображение товара'
            verbose_name_plural = 'Изображения товаров'

        def __str__(self):
            return u"изображение (id:%s)" % (self.pk)
