from typing import Any
from datetime import datetime, timedelta
from django import forms 

from .models import User 
from .shortcuts import DateInput


class UserLoginForm(forms.Form):
    email_address = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control inputarea email',    
                'placeholder': 'Enter Email Address',
                'id': 'email_address'
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control inputarea password',
                'placeholder': 'Enter Password Here',
                'id': 'password'
            }
        )
    )


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email_address', 'first_name', 'last_name', 'date_of_birth',)
        widgets = {
            'email_address': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Enter your email address',
                    'id': 'email_address'
                }
            ),
            'first_name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Enter your first name',
                    'id': 'first_name'
                }
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Enter your last name',
                    'id': 'last_name'
                }
            ),
            'date_of_birth': DateInput(
                attrs = {
                    'class': 'form-control',
                    'id': 'dob',
                    'max': (datetime.now()-timedelta(days=10*365)).strftime("%d/%m/%Y"),
                    'min': (datetime.now()-timedelta(days=70*365)).strftime("%d/%m/%Y")
                }
            )
        }


class UserPasswordRequestForm(forms.Form):

    email_address = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control email',    
                'placeholder': 'Enter Email Address',
                'id': 'email_address'
            }
        )
    )


class UserPasswordResetForm(forms.Form):

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control inputarea password',
                'placeholder': 'Enter Password Here',
                'id': 'password'
            }
        )
    )

    confirm_password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control inputarea password',
                'placeholder': 'Confirm Password',
                'id': 'confirmpassword'
            }
        )
    )

    def is_valid(self) -> bool:
        value: bool = super().is_valid()
        return value and (self.cleaned_data['password'] == self.cleaned_data['confirm_password'])
    

class UserSignupForm(forms.ModelForm):

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control inputarea password',
                'placeholder': 'Enter Password Here',
                'id': 'password'
            }
        )
    )

    confirm_password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control inputarea password',
                'placeholder': 'Confirm Password',
                'id': 'confirmpassword'
            }
        )
    )

    class Meta:
        model = User
        fields = ('email_address', 'first_name', 'last_name', 'date_of_birth',)
        widgets = {
            'email_address': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Enter your email address',
                    'id': 'email_address'
                }
            ),
            'first_name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Enter your first name',
                    'id': 'first_name'
                }
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Enter your last name',
                    'id': 'last_name'
                }
            ),
            'date_of_birth': DateInput(
                attrs = {
                    'class': 'form-control',
                    'id': 'dob',
                    'max': (datetime.now()-timedelta(days=10*365)).strftime("%d/%m/%Y"),
                    'min': (datetime.now()-timedelta(days=70*365)).strftime("%d/%m/%Y")
                }
            )
        }

    def save(self, commit: bool = ...) -> Any:
        instance = super().save(False)
        if commit:
            instance.set_password(self.cleaned_data['password'])
            instance.save()
            return instance
        return instance
