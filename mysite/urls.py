from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage

from .sitemaps import StaticViewSitemap

sitemaps = {
    'static' : StaticViewSitemap()
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')), 
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', include('main.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps, "template_name": "custom_sitemap.html"}, name="django.contrib.sitemaps.views.sitemap"),
    path('favicon.ico', RedirectView.as_view(url = staticfiles_storage.url('assets/img/favicon.ico'))),
    path('.well-known/discord', RedirectView.as_view(url = staticfiles_storage.url('main/assets/discord'))),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)