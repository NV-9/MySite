from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')), 
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('auth/', include('myauth.urls')),
    path('tutor/', include('tutor.urls')),
    path('', include('main.urls')),
    path('favicon.ico', RedirectView.as_view(url = staticfiles_storage.url('assets/img/favicon.ico'))),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

