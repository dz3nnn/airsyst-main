from django.conf import settings

from main.models import Brand, Equipment_Item, Certificate


def get_equipment_brands():
    brands_pk = Equipment_Item.objects.all().values_list("brand__pk", flat=True)
    return Brand.objects.filter(pk__in=brands_pk)


def get_certificates_for_current_lang():
    if settings.CURRENT_SITE_LANG == "ru":
        return Certificate.objects.filter(flag_ru=True)
    else:
        return Certificate.objects.filter(flag_en=True)
