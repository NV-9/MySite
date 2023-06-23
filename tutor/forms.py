from typing import Any
from .models import *
from django import forms 
import datetime 

class DateInput(forms.DateInput):
    input_type = 'date'



class AddLessonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.lessonplan_id:
            self.fields['paid'].queryset = Student.objects.filter(lessonplans=self.instance.lessonplan_id)

    recurring = forms.BooleanField(required = False)
    weeks = forms.IntegerField(min_value = 1, max_value = 52, required = False)

    class Meta:
        model = Lesson
        fields = ('start_time', 'end_time', 'paid', 'lessonplan')
        

    

    def save(self, commit: bool = ...) -> Any:
        if not self.cleaned_data['end_time']:
            instance: Lesson = super().save(False)
            instance.end_time = instance.start_time + instance.lessonplan.lesson_duration
            instance.save(commit)

        if self.cleaned_data['recurring'] == True:
            weeks = self.cleaned_data['weeks']
            if weeks >= 1 and weeks <= 52:
                instance: Lesson = super().save(commit)

                lessonplan = instance.lessonplan
                start_time = instance.start_time
                end_time = instance.end_time

                for i in range(1, weeks):
                    start_time = start_time + datetime.timedelta(weeks=1)
                    end_time = end_time + datetime.timedelta(weeks=1)

                    lesson = Lesson(start_time = start_time, end_time = end_time, lessonplan = lessonplan)
                    lesson.save()
                return instance
        return super().save(commit)













