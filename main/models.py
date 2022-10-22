from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from .utils import lat_to_cyr_slugify, get_slug_by_lang
from tinymce import models as tinymce_models
from django.utils.translation import gettext as _
from .utils import uuid_generator, article_generator
from django.conf import settings
from django.urls import reverse


SERVICE_CHOICES = (
    ("MAINTENANCE", _("Обслуживание")),
    ("REPAIR", _("Сервис")),
    ("SELL", _("Продажи")),
)

NO_IMAGE_URL = f"{settings.MEDIA_URL}category_images/no_image.jpg"


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="category_images", default="no_image.jpg")
    slug = models.SlugField(editable=False, unique=True)
    slug_ru = models.SlugField(editable=False, blank=True)
    parent = TreeForeignKey(
        "self", blank=True, null=True, related_name="child", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            "slug",
            "parent",
        )
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return " -> ".join(full_path[::-1])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.slug_ru = lat_to_cyr_slugify(self.name_ru)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.is_leaf_node():
            return reverse(
                "product-catalog-by-slug",
                kwargs={"category_slug": get_slug_by_lang(self)},
            )
        else:
            return reverse(
                "product-category-by-slug",
                kwargs={"category_slug": get_slug_by_lang(self)},
            )


class Country(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    flag = models.ImageField(
        upload_to="country_flags/", verbose_name="Флаг", null=True, blank=True
    )

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Бренд"""

    name = models.CharField(max_length=200, verbose_name="Название")
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name="Страна", null=True, blank=True
    )
    logo = models.FileField(
        upload_to="brand_logos/", verbose_name="Логотип", null=True, blank=True
    )

    @property
    def get_logo(self):
        if self.logo:
            return self.logo.url
        else:
            return NO_IMAGE_URL

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    logo = models.ImageField(
        upload_to="company_logos/", verbose_name="Логотип", null=True, blank=True
    )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name


class Project(models.Model):
    project_type = models.CharField(
        max_length=20,
        choices=SERVICE_CHOICES,
        verbose_name="Вид работ",
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд")
    date = models.DateField(verbose_name="Дата")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Организация"
    )
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    description = tinymce_models.HTMLField(
        verbose_name="Описание", null=True, blank=True
    )

    @property
    def get_first_image_url(self):
        images = Project_Image.objects.filter(project__pk=self.pk)
        if images:
            return images.first().image.url
        else:
            return NO_IMAGE_URL

    @property
    def get_all_images(self):
        images = Project_Image.objects.filter(project__pk=self.pk)
        return images

    def get_absolute_url(self):
        return reverse("project-single-page", kwargs={"project_id": self.pk})

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-date"]

    def __str__(self):
        return "%s - %s (№%s)" % (
            self.get_project_type_display(),
            self.company.name,
            self.pk,
        )


class Project_Image(models.Model):
    """Галерея проекта"""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="Проект"
    )
    image = models.ImageField(upload_to="project_images/", verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение проекта"
        verbose_name_plural = "Изображения проекта"

    def __str__(self):
        return "изображение (id:%s)" % (self.pk)


class Information(models.Model):
    ru = tinymce_models.HTMLField(verbose_name="ru site", null=True, blank=True)
    by = tinymce_models.HTMLField(verbose_name="by site", null=True, blank=True)
    ie = tinymce_models.HTMLField(verbose_name="ie site", null=True, blank=True)
    eu = tinymce_models.HTMLField(verbose_name="eu site", null=True, blank=True)
    description = models.CharField(
        max_length=250, verbose_name="Описание", null=True, blank=True
    )
    uid = models.TextField(primary_key=True, default=uuid_generator)

    class Meta:
        verbose_name = "Информация"
        verbose_name_plural = "Информация"

    def __str__(self):
        return "%s (uid:%s)" % (self.description, self.uid)


class Equipment_Item(models.Model):

    name = models.CharField(max_length=100, verbose_name="Название", null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name="Бренд", null=True, blank=True
    )
    country_create = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name="Страна изготовителя",
        null=True,
        blank=True,
    )
    article = models.CharField(max_length=8, verbose_name="Артикул", blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена поставщика (EUR)",
        null=True,
        blank=True,
    )
    delivery_time = models.CharField(
        max_length=100, verbose_name="Срок доставки", null=True, blank=True
    )
    supply_time = models.CharField(
        max_length=100, verbose_name="Срок поставки", null=True, blank=True
    )
    warranty = models.CharField(
        max_length=100, verbose_name="Гарантия", null=True, blank=True
    )

    weight = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Вес (кг)", null=True, blank=True
    )
    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Ширина (см)",
        null=True,
        blank=True,
    )
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Длина (см)",
        null=True,
        blank=True,
    )
    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Высота (см)",
        null=True,
        blank=True,
    )

    description = tinymce_models.HTMLField(
        verbose_name="Описание", null=True, blank=True
    )
    slug = models.SlugField(editable=False, unique=True, blank=True)
    slug_ru = models.SlugField(editable=False, blank=True)

    def get_absolute_url(self):
        return reverse(
            "product-card-by-article",
            kwargs={"product_article": self.article},
        )

    @property
    def get_first_image_url(self):
        images = Equipment_Image.objects.filter(equip__pk=self.pk)
        if images:
            return images.first().image.url
        else:
            return NO_IMAGE_URL

    @property
    def get_all_images_url(self):
        result = []
        images = Equipment_Image.objects.filter(equip__pk=self.pk)
        if images:
            for image in images:
                result.append(image.image.url)
        else:
            result.append(NO_IMAGE_URL)
        return result

    @property
    def get_final_price(self):
        if self.price:
            return self._calc_price(self.price)
        else:
            return _("On order")

    def _calc_price(self, price):
        valute = "EUR"
        return f"{price} {valute}"

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"

    def __str__(self):
        return "%s (art:%s)" % (self.name, self.article)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.slug_ru = lat_to_cyr_slugify(self.name_ru)

        if not self.article:
            art = article_generator()
            while Equipment_Item.objects.filter(article=art):
                art = article_generator()
            self.article = art

        super(Equipment_Item, self).save(*args, **kwargs)


class Equipment_Image(models.Model):
    equip = models.ForeignKey(
        Equipment_Item, on_delete=models.CASCADE, verbose_name="Проект"
    )
    image = models.ImageField(upload_to="equip_images/", verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение оборудования"
        verbose_name_plural = "Изображения оборудования"

    def __str__(self):
        return "изображение (id:%s)" % (self.pk)


class Option(models.Model):

    name = models.CharField(
        max_length=100, verbose_name="Характеристика", null=True, blank=True
    )
    numerical = models.BooleanField(verbose_name="Числовое", default=False)

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"
        ordering = ["name"]

    def __str__(self):
        return "%s" % (self.name)


class OptionValue(models.Model):
    """Значение характеристики"""

    name = models.CharField(
        max_length=100, verbose_name="Значение", null=True, blank=True
    )

    class Meta:
        verbose_name = "Значение характеристики"
        verbose_name_plural = "Значения характеристики"
        ordering = ["name"]

    def __str__(self):
        return "%s" % (self.name)


class OptionRelation(models.Model):
    """Связь характеристик"""

    equipment = models.ForeignKey(
        Equipment_Item,
        on_delete=models.CASCADE,
        verbose_name="Оборудование",
        null=True,
        blank=True,
    )
    option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        verbose_name="Характеристика",
        null=True,
        blank=True,
    )
    option_value = models.ForeignKey(
        OptionValue,
        on_delete=models.CASCADE,
        verbose_name="Значение",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Связь характеристик"
        verbose_name_plural = "Связи арактеристик"

    def __str__(self):
        return "%s(%s - %s)" % (
            self.equipment.name,
            self.option.name,
            self.option_value.name,
        )


class Certificate(models.Model):
    description = models.CharField(
        max_length=50, verbose_name="Описание", null=True, blank=True
    )
    image = models.ImageField(
        upload_to="certificate_images/",
        verbose_name="Изображение",
        null=True,
        blank=True,
    )
    equipment = models.ForeignKey(
        Equipment_Item,
        on_delete=models.PROTECT,
        verbose_name="Оборудование",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"

    def __str__(self):
        return "%s" % (self.description)
