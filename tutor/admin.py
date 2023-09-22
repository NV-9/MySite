from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from .models import * 
from .forms import *


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['lessonplan', 'start_time', 'end_time', 'paid']
    list_filter = ['start_time', 'end_time', 'paid']
    ordering = ['id', '-start_time']

    form = AddLessonForm


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'color']
    list_filter = ['student', 'course']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time']
    list_filter = ['clash']
    ordering = ['id', '-start_time']

    form = AddEventForm

admin.site.register(Course)
admin.site.register(Booking)

