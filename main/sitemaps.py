from django.contrib.sitemaps import Sitemap
from .models import Project, Equipment_Item
from django.urls import reverse


class BaseSitemap(Sitemap):
    protocol = "https"


class ProjectSitemap(BaseSitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Project.objects.all()


class ProductSitemap(BaseSitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Equipment_Item.objects.all()


class StaticSitemap(BaseSitemap):
    changefreq = "yearly"
    priority = 0.8

    def items(self):
        return ["index-page", "about-page"]

    def location(self, item):
        return reverse(item)
