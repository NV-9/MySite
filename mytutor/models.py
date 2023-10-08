import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.dispatch import receiver
import random 


from myauth.models import User 


def generate_color():
    return '#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])



class Student(models.Model):

    user = models.OneToOneField(User, verbose_name = 'User',related_name = 'student', on_delete = models.CASCADE)

    unpaid = models.IntegerField(verbose_name = 'Unpaid', default = 0)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return self.user.get_full_name()
    
    def lessons(self, paid: bool = None) -> QuerySet:
        q: QuerySet = self.lessonplan.none()
        match paid:
            case None:
                for lessonplan in self.lessonplan.all():
                    q = q.union(lessonplan.lesson.all())
            case _:
                for lessonplan in self.lessonplan.all():
                    q = q.union(lessonplan.lessons.filter(paid = paid))
        return q.order_by('start_time')
    
    def pay(self, value: int):
        for lesson in self.lessons(paid = False):
            if value >= lesson.fee:
                value -= lesson.fee
                lesson.pay()
            else:
                break
        pass 
                    
        
        


class Course(models.Model):

    subject = models.CharField(verbose_name = 'Name', max_length = 40)
    description = models.CharField(verbose_name = 'Description', max_length = 256)

    fee = models.PositiveIntegerField(verbose_name = 'Fee')

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return self.subject


class LessonPlan(models.Model):

    course = models.ForeignKey(Course, verbose_name = 'Course', on_delete = models.CASCADE, related_name = 'lessonplan')
    student = models.ForeignKey(Student, verbose_name = 'Student', on_delete = models.CASCADE, related_name = 'lessonplan')
    color = models.CharField(verbose_name = 'Colour', default = generate_color)

    class Meta:
        verbose_name = 'Lesson Plan'
        verbose_name_plural = 'Lesson Plans'
    
    def __str__(self):
        return f'{self.course} - {self.student}'
    
    @property 
    def colour(self):
        return self.color

    @property
    def fee(self):
        return self.course.fee



class Event(models.Model):

    start_time = models.DateTimeField(verbose_name = 'Start Time')
    end_time = models.DateTimeField(verbose_name = 'End Time')
    clash = models.BooleanField(verbose_name = 'Clash', default = True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
    
        conflicting_events = Event.objects.exclude(id=self.id).filter(
            clash = True,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if conflicting_events.exists() and not (self.start_time == conflicting_events.first().end_time or self.end_time == conflicting_events.last().start_time):
            raise ValidationError("Time Slot Unavailable")


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def next_week(self):
        next_lesson: Event = Event(start_time = self.start_time + datetime.timedelta(weeks=1), end_time = self.end_time + datetime.timedelta(weeks=1), clash = self.clash)     
        return next_lesson


class Lesson(Event):

    lessonplan = models.ForeignKey(LessonPlan, verbose_name = 'Lesson Plan', on_delete = models.CASCADE, related_name = 'lesson')
    paid = models.BooleanField(default = False)
    event = models.OneToOneField(Event, parent_link = True, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
    
    def __str__(self):
        return f"{self.lessonplan} | {self.start_time} to {self.end_time}"

    @property
    def fee(self):
        return self.lessonplan.fee
    
    def next_week(self):
        next_lesson: Lesson = Lesson(lessonplan = self.lessonplan, start_time = self.start_time + datetime.timedelta(weeks=1), end_time = self.end_time + datetime.timedelta(weeks=1), clash = self.clash)     
        return next_lesson

    def clean(self):
        super().clean()
        
        conflicting_lessons = Lesson.objects.exclude(id=self.id).filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if conflicting_lessons.exists() and self.lessonplan != conflicting_lessons.first().lessonplan and self.clash == True:
            raise ValidationError("This lesson clashes with another lesson.")

    def pay(self):
        if self.paid != True:
            self.lessonplan.student.unpaid -= self.fee 
            self.paid = True
            check = self.save()
            if check:
                self.lessonplan.student.save()
            return True 
        return False









class Booking(models.Model):

    student = models.ForeignKey(Student, on_delete = models.CASCADE, related_name = 'bookings')
    start_time = models.DateTimeField(verbose_name = 'Start Time')
    end_time = models.DateTimeField(verbose_name = 'End Time')

    

@receiver(models.signals.post_save, sender = User)
def create_auth(sender, instance: User, created, **kwargs):
    if created:
        Student.objects.create(user = instance)


@receiver(models.signals.post_save, sender = Lesson)
def new_lesson(sender, instance: Lesson, created, **kwargs):
    if created:
        instance.lessonplan.student.unpaid += instance.fee
        instance.lessonplan.student.save()
        instance.save()


@receiver(models.signals.pre_delete, sender = Lesson)
def delete_lesson(sender, instance: Lesson, **kwargs):
    if instance.start_time >= datetime.datetime.now(datetime.timezone.utc):
        instance.lessonplan.student.unpaid -= instance.fee
        instance.lessonplan.student.save()

