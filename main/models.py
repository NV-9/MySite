from django.db import models
from django.utils import timezone


class ContactMessages(models.Model):

    name = models.CharField(max_length = 50, verbose_name = 'Name')
    email = models.EmailField(verbose_name = 'Email')
    subject = models.CharField(max_length = 200, verbose_name = 'Subject')
    content = models.CharField(max_length = 2000, verbose_name = 'Content')
    ip = models.GenericIPAddressField(verbose_name = 'IP', null = True)
    read = models.BooleanField(default = False)
    timestamp = models.DateTimeField(default = timezone.now)


    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
