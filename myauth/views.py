from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.base import RedirectView
from typing import Any
from django_hosts.resolvers import reverse

from .forms import UserEditForm, UserLoginForm, UserPasswordRequestForm, UserPasswordResetForm, UserSignupForm
from .models import random_token, User
from .shortcuts import AuthorisedUpdateView, UnauthorisedFormView, EmailThread


class AuthRedirectView(RedirectView):
    url = 'login'

class AuthLogoutView(RedirectView):
    url = '/'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        logout(request)
        return redirect(reverse('home', host = 'www'))

class AuthLoginView(UnauthorisedFormView):
    form_class = UserLoginForm
    template_name = 'myauth/login.html'
    success_url = 'profile'

    def form_valid(self, form: Any, request: HttpRequest) -> HttpResponse:
        email_address = form.cleaned_data['email_address']
        password = form.cleaned_data['password']
        try:
            user: User = User.objects.get(email_address = email_address)
            
            if check_password(password, user.password):
                if user.is_verified or user.is_staff:
                    login(request, user)
                    return redirect(self.get_success_url())
        except:
            form.add_error('email_address', 'User with that email address does not exist / Password incorrect!')
        return super().form_valid(form, request)

    def form_invalid(self, form: Any, request: HttpRequest) -> HttpResponse:
        form.add_error('email_address', 'User with that email address does not exist / Password incorrect!')
        return super().get(request)

class AuthProfileView(AuthorisedUpdateView):
    form_class = UserEditForm
    model = User 
    template_name = 'myauth/profile.html'
    success_url = 'profile'

class AuthPasswordRequestView(UnauthorisedFormView):
    form_class = UserPasswordRequestForm
    template_name = 'myauth/reset-request.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('logout')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        token = kwargs.pop('token', None)
        if token:
            try:
                user: User = User.objects.get(reset_password_token = token)
                user.reset_instance_token = random_token()
                user.save()
                return redirect(f'/auth/resetpassword/{user.reset_instance_token}/')
            except:
                pass
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: Any, request: HttpRequest) -> HttpResponse:
        email_address = form.cleaned_data['email_address']
        try:
            user: User = User.objects.get(email_address = email_address)
            user.reset_password()
            path =  request.build_absolute_uri()
            link = f'{path}{user.reset_password_token}'
            user.send_email_to_me('myauth/email-reset-request.html', 'Password Reset Request', {'url': link})            
        except:
            pass
        return render(request, template_name = 'myauth/check-email.html', context = {'title': 'Check Email for Reset','text': 'If your email matches one in our records, please check it to reset your password!'})

class AuthPasswordResetView(UnauthorisedFormView):
    form_class = UserPasswordResetForm
    template_name = 'myauth/reset-password.html'
    success_url = 'login'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        instance = kwargs.pop('instance', None)
        if instance:
            if User.objects.filter(reset_instance_token = instance).count() > 0:
                return render(request, self.template_name, context = {'form': self.form_class(request.POST or None)})
        return redirect('/')
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:   
        request.instance = kwargs.get('instance', None)     
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: Any, request: HttpRequest) -> HttpResponse:
        password = form.cleaned_data['password']
        try:
            user: User = User.objects.get(reset_instance_token = getattr(request, 'instance', 'invalid'))
            user.change_password(password)
            user.send_email_to_me('myauth/email-password-change.html', 'Password Changed')
            return redirect(self.get_success_url())
        except:
            pass 
        self.context = {'error': 'Passwords do not match', 'form': self.form_class()}
        return redirect('/')

class AuthSignupView(UnauthorisedFormView):
    form_class = UserSignupForm
    template_name = 'myauth/signup.html'
    success_url = 'login'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        token = kwargs.pop('token', None)
        if token:
            try:
                user: User = User.objects.get(verification_token = token)
                user.verification_token = None
                user.is_verified = True
                user.save()
                return redirect(self.get_success_url())
            except:
                return redirect('signup')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: Any, request: HttpRequest) -> HttpResponse:
        user: User = form.save()
        user.verification_token = random_token()
        user.save()

        path =  request.build_absolute_uri()
        link = f'{path}{user.verification_token}'
        from_email = settings.EMAIL_SEND_USER
        subject = 'Signup Verification'
        html_content = render_to_string('myauth/email-verification.html', {'url': link})
        text_content = strip_tags(html_content)
        EmailThread(subject, html_content, text_content, [user.email_address], from_email).start()
        
        return render(request, 'myauth/check-email.html', context = {'title': 'Check Email for Verification', 'text': 'A verification link has been sent to your email address. Please check your inbox and follow the instructions to verify your account.'})

    def form_invalid(self, form: Any, request: HttpRequest) -> HttpResponse:
        return super().form_invalid(form, request)

