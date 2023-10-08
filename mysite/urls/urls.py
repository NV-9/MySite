from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.sitemaps.views import sitemap
from django_hosts.resolvers import reverse
from django.shortcuts import redirect

from ..sitemaps import StaticViewSitemap

sitemaps = {
    'static' : StaticViewSitemap()
}

infopatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps, "template_name": "custom_sitemap.html"}, name="django.contrib.sitemaps.views.sitemap"),
    path('favicon.ico', RedirectView.as_view(url = staticfiles_storage.url('main/assets/img/favicon.ico'))),
    path('.well-known/discord', RedirectView.as_view(url = staticfiles_storage.url('main/assets/discord'))),
]

urlpatterns = [
    path('', include('main.urls')),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) + infopatterns