import datetime
from django.shortcuts import redirect
from django.views.generic.base import RedirectView, TemplateView

from myauth.shortcuts import *
from .models import Lesson


class TutoringView(RedirectView):
    url = 'calendar/'


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




