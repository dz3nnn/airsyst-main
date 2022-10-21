from django.contrib.sitemaps import Sitemap
from .models import Project
from django.urls import reverse


class ProjectSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Project.objects.all()

    # def lastmod(self, obj):
    #     return obj.pub_date


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    # protocol = "https"

    def items(self):
        return ["index-page", "about-page"]

    def location(self, item):
        return reverse(item)
