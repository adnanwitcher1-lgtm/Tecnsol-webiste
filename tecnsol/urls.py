from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

from core.sitemaps import sitemaps


def google_verification(request):
    # Google Search Console ownership verification (HTML file method).
    # Keep this route even after verification succeeds.
    return HttpResponse(
        "google-site-verification: googleebf7b0c35e3712d4.html",
        content_type="text/html",
    )


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /services/*/download/",
        "Allow: /",
        "",
        "Sitemap: https://tecnsoltraining.com/sitemap.xml",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path('googleebf7b0c35e3712d4.html', google_verification),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)