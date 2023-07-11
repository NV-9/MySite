from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserSignupForm
from .models import User
from tutor.models import Student


class StudentInline(admin.TabularInline):
    model = Student

@admin.register(User)
class MyUserAdmin(UserAdmin):

    list_display = ['email_address', 'id', 'first_name', 'last_name']
    list_filter = ['last_name', 'is_verified']
    ordering = ['id',]
    
    fieldsets = (
        (
            'Identification', {
                'fields': (
                    ('id', 'user_uuid',),
                )
            }
        ),
        (
            'Personal Information', {
                'fields': (('email_address', 'date_of_birth'), ('first_name', 'last_name'),),
            }
        ),
        (
            'Permissions', {
                'fields': (('is_active','is_staff',)),
            }
        ),
        (
            'Verification', {
                'fields': (('is_verified', 'verification_token'), ('reset_password_token', 'reset_instance_token')),
            }
        ),
        (
            'Log', {
                'fields': (('created_at', 'updated_at'), ('last_login', 'password_reset_at'),),
            }
        ),
    )
    readonly_fields = ['id', 'user_uuid', 'created_at', 'updated_at', 'last_login', 'password_reset_at']
    inlines = [StudentInline]

    add_form = UserSignupForm
    add_fieldsets = (
        (
            'Details', {
            'fields': (
                ('email_address', 'date_of_birth'), 
                ('first_name', 'last_name'), 
                ),
            }
        ),
        (
            'Password', {
                'fields': (
                    ('password', 'confirm_password'),
                ),
            }
        )
    )

    filter_horizontal = []
    