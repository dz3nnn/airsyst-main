from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category


class CategoryAdmin(MPTTModelAdmin):
    readonly_fields = ('slug', 'slug_ru')


admin.site.register(Category, CategoryAdmin)
