from main.models import Brand, Equipment_Item


def get_equipment_brands():
    brands_pk = Equipment_Item.objects.all().values_list("brand__pk", flat=True)
    return Brand.objects.filter(pk__in=brands_pk)
