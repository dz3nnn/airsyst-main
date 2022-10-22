from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from main.sitemaps import StaticSitemap, ProjectSitemap, ProductSitemap

from django.contrib.sitemaps.views import sitemap

sitemaps = {
    "static": StaticSitemap,
    "projects": ProjectSitemap,
    "products": ProductSitemap,
}

urlpatterns = (
    [
        path("tinymce/", include("tinymce.urls")),
        path("admin/", admin.site.urls),
        path("", include("main.urls")),
        path(
            "sitemap.xml",
            sitemap,
            {"sitemaps": sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)


handler404 = "main.views.page_404"
handler500 = "main.views.page_500"
