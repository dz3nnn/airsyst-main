from dataclasses import field
from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Project, Brand, Company, Country


class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Category, CategoryTranslationOptions)


class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "description")


translator.register(Project, ProjectTranslationOptions)


class BrandTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Brand, BrandTranslationOptions)


class CompanyTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Company, CompanyTranslationOptions)


class CountryTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Country, CountryTranslationOptions)
