from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (
    Category,
    Brand,
    Country,
    Company,
    Project,
    Project_Image,
    Information,
    Option,
    OptionRelation,
    OptionValue,
    Equipment_Image,
    Equipment_Item,
    Certificate,
)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    readonly_fields = ("slug", "slug_ru")


@admin.register(
    Brand,
    Company,
    Country,
    Project_Image,
    Information,
    Option,
    OptionRelation,
    OptionValue,
)
class DefaultAdmin(admin.ModelAdmin):
    pass


class ProjectImageInline(admin.StackedInline):
    model = Project_Image
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]


class EquipImageInline(admin.StackedInline):
    model = Equipment_Image
    extra = 1


class CertificateInline(admin.StackedInline):
    model = Certificate
    extra = 1


class OptionRelationInline(admin.StackedInline):
    model = OptionRelation
    extra = 1

    def formfield_for_forei1gnkey(self, db_field, request, **kwargs):
        if db_field.name == "option_value":
            if self.object.option:
                kwargs["queryset"] = OptionValue.objects.filter(pk=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Equipment_Item)
class EquipmentItemAdmin(admin.ModelAdmin):
    inlines = [OptionRelationInline, EquipImageInline, CertificateInline]
    search_fields = ["article"]
    readonly_fields = ["article"]
