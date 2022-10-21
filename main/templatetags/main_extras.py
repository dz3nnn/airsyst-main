from django import template
from main.models import Category, Information
from django.conf import settings
from ..utils import get_model_attr_by_lang
import re
from typing import List

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
    # <p>Some text</p>
    if info_text:
        first_tag = info_text.find(">")
        last_tag = info_text.rfind("<")
        if first_tag > 0 and last_tag > 0:
            return info_text[first_tag + 1 : last_tag]
    return info_text


@register.filter(name="get_info_by_uid")
def get_info_by_uid(info_uid: str) -> str:
    # ru,by,ie,eu
    info = Information.objects.filter(uid=info_uid)
    if info:
        first_info = info.first()
        if settings.CURRENT_SITE_REGION == "eu":
            return remove_root_tag(first_info.eu)
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
