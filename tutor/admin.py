from django.contrib import admin
from .models import * 
from .forms import *

admin.site.register(LessonPlan)
admin.site.register(Student)
admin.site.register(Course)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    form = AddLessonForm
    ordering = ['-start_time']

