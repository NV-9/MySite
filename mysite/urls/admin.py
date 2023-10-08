from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', admin.site.urls, name = 'admin'),
    path('', include('jet.urls', 'jet')), 
]