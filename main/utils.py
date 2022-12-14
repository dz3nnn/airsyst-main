from django.utils.text import slugify as django_slugify
from django.conf import settings

import uuid
import random

# Slugify (Cyrillic)
alphabet = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ы": "i",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def lat_to_cyr_slugify(s):
    return django_slugify("".join(alphabet.get(w, w) for w in s.lower()))


def uuid_generator():
    return uuid.uuid4().hex


def get_slug_by_lang(_obj):
    try:
        if settings.CURRENT_SITE_LANG == "ru":
            return getattr(_obj, f"slug_ru")
        else:
            return getattr(_obj, f"slug")
    except AttributeError:
        return ""


def get_model_attr_by_lang(_obj, _field):
    try:
        if settings.CURRENT_SITE_LANG == "ru":
            return getattr(_obj, f"{_field}_ru")
        else:
            return getattr(_obj, f"{_field}_en")
    except AttributeError:
        return ""


def get_model_attr_by_region(_obj, _field, remove_root=False):
    try:
        if settings.CURRENT_SITE_REGION:
            if not remove_root:
                return getattr(_obj, f"{_field}_{settings.CURRENT_SITE_REGION}")
            else:
                return remove_root_tag_func(
                    getattr(_obj, f"{_field}_{settings.CURRENT_SITE_REGION}")
                )
    except AttributeError:
        return ""


def remove_root_tag_func(info_text: str) -> str:
    # <p>Some text</p>
    if info_text:
        first_tag = info_text.find(">")
        last_tag = info_text.rfind("<")
        if first_tag > 0 and last_tag > 0:
            return info_text[first_tag + 1 : last_tag]
    return info_text


def get_template_for_lang(template_name):
    if settings.CURRENT_SITE_LANG == "ru":
        return f"{template_name}_ru.html"
    else:
        return f"{template_name}.html"


def message_to_managers():
    pass


def article_generator():
    return f"{random_upper_letter()}{random_upper_letter()}{str(random.randrange(10000)).zfill(4)}"


def random_upper_letter():
    return chr(random.randint(ord("A"), ord("Z")))
