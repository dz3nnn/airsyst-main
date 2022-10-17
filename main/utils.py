from django.utils.text import slugify as django_slugify
from django.conf import settings
import uuid

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


def get_model_attr_by_lang(_obj, _field):
    try:
        if settings.CURRENT_SITE_LANG == "ru":
            return getattr(_obj, f"{_field}_ru")
        else:
            return getattr(_obj, f"{_field}_en")
    except AttributeError:
        return ""


def get_template_for_lang(template_name):
    if settings.CURRENT_SITE_LANG == "ru":
        return f"{template_name}_ru.html"
    else:
        return f"{template_name}.html"
