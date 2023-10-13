from django.urls import path 
from .views import post_view


urlpatterns = [
    path('<slug:slug>/', post_view, name = 'post'),
    path('', post_view, name = 'blog'),
]