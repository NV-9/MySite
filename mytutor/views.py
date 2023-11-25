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
        return ['mytutor/tutor.html']
    

class CalendarView(AuthorisedFormView):
    template_name = 'mytutor/calendar.html'
    form_class = LessonBookingForm
    success_url = '/'
    
    def get(self, request, *args, **kwargs):
        student = getattr(request.user, 'student', None)
        if not student and not request.user.is_staff:
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {
            'events': Event.objects.filter(start_time__gte=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days = 180))
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
        start_time = datetime.datetime.combine(form.cleaned_data['date'], form.cleaned_data['start_time'])
        end_time = datetime.datetime.combine(form.cleaned_data['date'], form.cleaned_data['end_time'])
        Booking.objects.create(start_time = start_time, end_time = end_time, student = request.user.student)
        return super().form_valid(form, request)


class StudentView(AuthorisationMixin, DetailView):
    template_name = 'mytutor/studentview.html'
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
        lesson_id = request.POST.get('lesson_id')
        try:
            lesson: Lesson = Lesson.objects.get(pk = lesson_id)
            success = lesson.pay()
            return JsonResponse({'success': success})
        except:
            return JsonResponse({'success': False})


class StudentsView(AuthorisationMixin, ListView):
    model = Student 
    template_name = 'mytutor/students.html'
    context_object_name = 'students'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        student: Student = Student.objects.get(pk = 2)
        return super().get(request, *args, **kwargs)

    def get_template_names(self) -> List[str]:
        return ['mytutor/students.html']


def booking_view(request: HttpRequest):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('tutor')

    if request.method == "POST":
        bid = request.POST.get('booking_id', None)
        if bid is not None:
            opts = Booking.objects.filter(pk = bid)

            if len(opts) >= 1:
                booking: Booking = opts[0]
                plan = booking.student.lessonplan.first()
                if plan:
                    lesson = Lesson.objects.create(lessonplan = plan, start_time = booking.start_time, end_time = booking.end_time)
                    lesson.save()
                    booking.delete()
                    return JsonResponse({"success": True})
        
        return JsonResponse({"success": False})
    bookings = Booking.objects.all()
    return render(request, "mytutor/booking.html", context = {'bookings': bookings})

