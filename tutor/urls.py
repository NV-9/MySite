from django.urls import path 
from .views import *

urlpatterns = [
    path('', TutoringView.as_view(), name = 'tutor'),
    path('calendar/', CalendarView.as_view(), name = 'calendar'),
    path('student/', StudentsView.as_view(), name = 'students'),
    path('student/<uuid:uuid>', StudentView.as_view(), name = 'studentview')
]
