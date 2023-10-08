from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name = 'www'),
    host(r'admin', 'mysite.urls.admin', name = 'admin'),
    host(r'auth', 'myauth.urls', name = 'auth'),
    host(r'tutor', 'mytutor.urls', name = 'tutor'),
    host(r'api', 'myapi.urls', name = 'api'),
    host(r'blog', 'myblog.urls', name = 'blog'),
)
