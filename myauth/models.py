from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid
import random 
from .shortcuts import EmailThread


def random_token(length: int = 40):
    return "".join(list(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length)))


class UserManager(BaseUserManager):

    def create_user(self, email_address, date_of_birth, first_name, last_name, password = None, **kwargs):
        user = self.model(
            email_address = email_address,
            date_of_birth = date_of_birth,
            first_name = first_name,
            last_name = last_name,
            **kwargs
        )
        user.set_password(password)
        user.save(using = self._db)
        return user 

    def create_superuser(self, email_address, date_of_birth, first_name, last_name, password = None):
        user = self.create_user(email_address, date_of_birth, first_name, last_name, password)
        user.is_staff = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):

    id        = models.AutoField(primary_key = True)
    user_uuid = models.UUIDField(verbose_name = 'User UUID', default = uuid.uuid4, editable = False)

    email_address  = models.EmailField(verbose_name = 'Email Address', max_length = 255, unique = True)
    date_of_birth  = models.DateField(verbose_name = 'Date of Birth')
    first_name     = models.CharField(verbose_name = 'First Name', max_length = 255)
    last_name      = models.CharField(verbose_name = 'Last Name', max_length = 255)

    is_active = models.BooleanField(verbose_name = 'Account Active?', default = True)
    is_staff  = models.BooleanField(verbose_name = 'Account Admin?',  default = False)
    is_verified = models.BooleanField(verbose_name = 'Account Verified?', default = False)

    created_at = models.DateTimeField(verbose_name = 'Created At', auto_now_add = True)
    updated_at = models.DateTimeField(verbose_name = 'Created At', auto_now_add = True)

    verification_token = models.CharField(verbose_name = 'Verfication Token', max_length = 200, null = True, blank = True)
    reset_password_token =  models.CharField(verbose_name = 'Reset Password Token', max_length = 200, null = True, blank = True)
    reset_instance_token = models.CharField(verbose_name = 'Reset Instance Token', max_length = 200, null = True, blank = True)
    password_reset_at = models.DateTimeField(null = True,  blank = True)

    objects = UserManager()

    USERNAME_FIELD = 'email_address'
    EMAIL_FIELD = 'email_address'
    REQUIRED_FIELDS = ['date_of_birth', 'first_name', 'last_name']

    def has_perm(self, perm, obj=None): 
        return True
    def has_module_perms(self, app_label): 
        return True
    
    def __str__(self):
        return self.email_address
    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def send_email_to_me(self, file_path: str, subject: str, context: dict = None):
        context = context or {}
        html_content = render_to_string(file_path, context)
        text_content = strip_tags(html_content)
        EmailThread(subject, html_content, text_content, [self.email_address], settings.EMAIL_SEND_USER).start()

    def reset_password(self):
        self.reset_password_token = random_token()
        self.save()

    def reset_instance(self):
        self.reset_instance_token = random_token()
        self.save()

    def change_password(self, password: str):
        self.set_password(password)
        self.reset_instance_token = None 
        self.reset_password_token = None
        self.save()
