import datetime
from typing import List
from django.shortcuts import redirect
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic import ListView

from myauth.shortcuts import *
from .models import Lesson, Course


class TutoringView(RedirectView):
    url = 'calendar/'


class TutoringView(TemplateView):
    template_name = 'tutor/tutor.html'

    def get(self, request, *args, **kwargs):
        student = getattr(request.user, 'student', None)
        if not student and not request.user.is_staff:
            return redirect('/')
        courses = Course.objects.all()
        context = {
            'courses': courses
        }
        kwargs.update(context)
        return super().get(request, *args, **kwargs)

class TutoringView(ListView):
    model = Course
    context_object_name = 'courses'
    
    def get_template_names(self) -> List[str]:
        return ['tutor/tutor.html']



    

class CalendarView(AuthorisationMixin, TemplateView):
    template_name = 'tutor/calendar.html'
    
    def get(self, request, *args, **kwargs):
        student = getattr(request.user, 'student', None)
        if not student and not request.user.is_staff:
            return redirect('/')
        events = Lesson.objects.filter(start_time__gte=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days = 60))
        context = {
            'events': events
        }
        kwargs.update(context)
        return super().get(request, *args, **kwargs)




