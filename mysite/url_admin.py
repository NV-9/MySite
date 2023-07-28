from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', admin.site.urls),
    path('', include('jet.urls', 'jet')), 
    path('dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
]