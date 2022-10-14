from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Brand, Country, Company, Project, Project_Image, Information


class CategoryAdmin(MPTTModelAdmin):
    readonly_fields = ('slug', 'slug_ru')


admin.site.register(Category, CategoryAdmin)


@admin.register(Brand, Company, Country, Project, Project_Image, Information)
class DefaultAdmin(admin.ModelAdmin):
    pass
