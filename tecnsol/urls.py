from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static


def google_verification(request):
    # Google Search Console ownership verification (HTML file method).
    # Keep this route even after verification succeeds.
    return HttpResponse(
        "google-site-verification: googleebf7b0c35e3712d4.html",
        content_type="text/html",
    )


urlpatterns = [
    path('googleebf7b0c35e3712d4.html', google_verification),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)