from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *


admin.site.register(ContactMessages)
admin.site.unregister(Group)