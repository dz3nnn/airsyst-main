from django import template
from django.conf import settings
from typing import List
from django.db.models import Q

import re

from main.models import Category, Information, Option, OptionRelation, OptionValue
from main.utils import (
    get_model_attr_by_lang,
    get_model_attr_by_region,
    remove_root_tag_func,
)
from main.helps import to_float

register = template.Library()

MONTHS_RU = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]

MONTHS = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]


@register.filter
def get_day(value):
    """Get day from date"""
    result = value.strftime("%d")
    if len(result) < 2:
        result = "0" + result
    return result


@register.filter
def get_month(value):
    """Get month from date"""
    if settings.CURRENT_SITE_LANG == "ru":
        return MONTHS_RU[value.month - 1]
    else:
        return MONTHS[value.month - 1]


@register.filter
def get_year(value):
    """Get year from date"""
    return value.year


@register.filter(name="get_category_slug_for_lang")
def get_category_slug_for_lang(category_model: Category) -> str:
    if settings.CURRENT_SITE_LANG == "ru":
        return category_model.slug_ru
    else:
        return category_model.slug


@register.filter(name="remove_root_tag")
def remove_root_tag(info_text: str) -> str:
    return remove_root_tag_func(info_text)


@register.filter(name="get_info_by_uid")
def get_info_by_uid(info_uid: str) -> str:
    # ru,by,ie,eu
    info = Information.objects.filter(uid=info_uid)
    if info:
        first_info = info.first()
        return get_model_attr_by_region(first_info, "info", True)
    return ""


@register.filter(name="split")
def split(value):
    return value.split(" ")


@register.simple_tag
def define(val=None):
    return val


@register.filter
def trim_phone_for_tag(value):
    return re.sub("[^0-9+]", "", value)


@register.filter(name="get_lang_field")
def get_object_attr_for_lang(value, arg):
    return get_model_attr_by_lang(value, arg)


@register.filter
def have_childs(value: Category) -> bool:
    return not value.is_leaf_node()


@register.filter
def get_parent_categories(value: Category) -> List[Category]:
    if value:
        return value.get_family()


# Old


@register.simple_tag
def get_min_value_for_option(option_id, items):
    items_pk = items.values_list("pk", flat=True)
    relations = OptionRelation.objects.filter(equipment__pk__in=items_pk).values_list(
        "option_value__pk"
    )
    opt_values = OptionValue.objects.filter(pk__in=relations).values_list(
        "name", flat=True
    )
    float_values = to_float(opt_values)
    return min(float_values, default=0)


@register.simple_tag
def get_max_value_for_option(option_id, items):
    items_pk = items.values_list("pk", flat=True)
    relations = OptionRelation.objects.filter(equipment__pk__in=items_pk).values_list(
        "option_value__pk"
    )
    opt_values = OptionValue.objects.filter(pk__in=relations).values_list(
        "name", flat=True
    )
    float_values = to_float(opt_values)
    return max(float_values, default=0)


@register.simple_tag
def get_option_values(equips, option_id):
    equips_id = equips.values_list("pk", flat=True)
    relations = (
        OptionRelation.objects.filter(equipment__pk__in=equips_id, option__pk=option_id)
        .values_list("option_value_id", flat=True)
        .distinct()
    )
    result = OptionValue.objects.filter(pk__in=relations).order_by("name")
    return result
