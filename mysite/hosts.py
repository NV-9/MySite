from django_hosts import patterns, host
from django.conf import settings
from django.contrib import admin

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name = 'www'),
    host(r'admin', 'mysite.url_admin', name = 'admin'),
    host(r'auth', 'myauth.urls', name = 'auth'),
    host(r'tutor', 'tutor.urls', name = 'tutor'),
    host(r'api', 'myapi.urls', name = 'api'),
)

