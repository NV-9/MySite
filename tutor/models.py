from django.db import models
from myauth.models import User 
import random 

def generate_color():
    return '#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])


class Course(models.Model):
    
    description = models.CharField()
    fee = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return self.description


class Student(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'student')
    overflow = models.IntegerField(default = 0)
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students' 
    
    def __str__(self):
        return self.user.get_full_name()


class LessonPlan(models.Model):

    start_date = models.DateField(auto_now_add = True)
    lesson_duration = models.DurationField()
    course = models.ForeignKey(Course, related_name = 'lessonplans', on_delete = models.CASCADE)
    student = models.ManyToManyField(Student, related_name = 'lessonplans')
    color = models.CharField(default = generate_color)

    def __str__(self):
        return f"{self.course} - ({self.clean_students()})"
    
    
    def clean_students(self):
        return ", ".join([str(s) for s in self.student.all()])


class Lesson(models.Model):
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank = True)
    lessonplan = models.ForeignKey(LessonPlan, on_delete = models.CASCADE, related_name = 'lessons')
    paid = models.ManyToManyField(Student, related_name='paid_lessons')

    def __str__(self):
        return f"{self.lessonplan} | {self.start_time} to {self.end_time} "

    
    











