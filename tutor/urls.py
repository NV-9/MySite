from django.urls import path 
from .views import *

urlpatterns = [
    path('', TutoringView.as_view(), name = 'tutoring'),
    path('calendar/', CalendarView.as_view(), name = 'calendar'),
]
