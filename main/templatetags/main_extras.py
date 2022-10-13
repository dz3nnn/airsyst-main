from django import template
from main.models import Category
from django.conf import settings

register = template.Library()


@register.filter(name='get_category_slug_for_lang')
def get_category_slug_for_lang(category_model: Category) -> str:
    if settings.CURRENT_SITE_LANG == 'ru':
        return category_model.slug_ru
    else:
        return category_model.slug
