from typing import Any
from django import forms 

from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class AddLessonForm(forms.ModelForm):

    recurring = forms.BooleanField(required = False)
    weeks = forms.IntegerField(min_value = 1, max_value = 52, required = False)

    class Meta:
        model = Lesson
        fields = ('start_time', 'end_time', 'clash', 'paid', 'lessonplan')
            

    def save(self, commit: bool = ...) -> Any:
        
        if self.cleaned_data['recurring'] == True:
            weeks = self.cleaned_data['weeks']
            if 1 <= weeks <= 52:
                instance: Lesson = super().save(commit)
                next = instance
                for _ in range(0, weeks):
                    next = next.next_week()
                    next.save()
                return instance
        
        return super().save(commit)

   
class EditLessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ('start_time', 'end_time', 'clash', 'paid', 'lessonplan')


class LessonBookingForm(forms.Form):

    date = forms.DateField(widget = forms.DateInput(attrs = {'type': 'date'}))
    start_time = forms.TimeField(widget = forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget = forms.TimeInput(attrs={'type': 'time'}))
