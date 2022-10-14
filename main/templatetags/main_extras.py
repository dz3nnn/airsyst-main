from django import template
from main.models import Category, Information
from django.conf import settings

register = template.Library()


@register.filter(name='get_category_slug_for_lang')
def get_category_slug_for_lang(category_model: Category) -> str:
    if settings.CURRENT_SITE_LANG == 'ru':
        return category_model.slug_ru
    else:
        return category_model.slug


@register.filter(name='remove_root_tag')
def remove_root_tag(info_text: str) -> str:
    # <p>Some text</p>
    if info_text:
        first_tag = info_text.find('>')
        last_tag = info_text.rfind('<')
        if first_tag > 0 and last_tag > 0:
            return info_text[first_tag+1:last_tag]
    return info_text


@register.filter(name='get_info_by_uid')
def get_info_by_uid(info_uid: str) -> str:
    # ru,by,ie,eu
    info = Information.objects.filter(uid=info_uid)
    if info:
        first_info = info.first()
        if settings.CURRENT_SITE_REGION == 'eu':
            return first_info.eu
    return ''


@register.filter(name='split')
def split(value):
    return value.split(' ')


@register.simple_tag
def define(val=None):
    return val
