import datetime
from typing import Any, Dict, List
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView

from myauth.shortcuts import *
from .models import Lesson, Course, Student, Event, Booking
from .forms import LessonBookingForm



class TutoringView(ListView):
    model = Course
    context_object_name = 'courses'
    
    def get_template_names(self) -> List[str]:
        return ['tutor/tutor.html']
    

class CalendarView(AuthorisedFormView):
    template_name = 'tutor/calendar.html'
    form_class = LessonBookingForm
    success_url = '/'
    
    def get(self, request, *args, **kwargs):
        student = getattr(request.user, 'student', None)
        if not student and not request.user.is_staff:
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {
            'events': Event.objects.filter(start_time__gte=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days = 60))
        }      
        kwargs.update(context)
        return super().get_context_data(**kwargs)


    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES or None)
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form, request)
    
    def form_valid(self, form: Any, request: HttpRequest) -> HttpResponse:
        instance: Booking = form.save(commit = False)
        instance.student = request.user.student
        instance.save()
        return super().form_valid(form, request)


class StudentView(AuthorisationMixin, DetailView):
    template_name = 'tutor/studentview.html'
    model = Student
    context_object_name = 'student'
    slug_field = 'user__user_uuid'
    slug_url_kwarg = 'uuid'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            return redirect('/')
        if request.method == "POST":
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        print(args)
        print(request.POST)
        lesson_id = request.POST.get('lesson_id')
        try:
            lesson: Lesson = Lesson.objects.get(pk = lesson_id)
            success = lesson.pay()
            return JsonResponse({'success': success})
        except:
            return JsonResponse({'success': False})





class StudentsView(AuthorisationMixin, ListView):
    model = Student 
    template_name = 'tutor/students.html'
    context_object_name = 'students'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        student: Student = Student.objects.get(pk = 2)
        return super().get(request, *args, **kwargs)

    def get_template_names(self) -> List[str]:
        return ['tutor/students.html']
