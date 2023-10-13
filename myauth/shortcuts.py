# ABC View Templates
# 2 branches: unauthorised and authorised

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse 
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, UpdateView
import threading
from typing import Any
from django_hosts.resolvers import reverse
from functools import wraps
from urllib.parse import urlparse
from django.contrib.auth import REDIRECT_FIELD_NAME


def user_passes_test(
    test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME
):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = reverse('login', host = 'auth')
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (not login_scheme or login_scheme == current_scheme) and (
                not login_netloc or login_netloc == current_netloc
            ):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(path, resolved_login_url, redirect_field_name)

        return _wrapper_view

    return decorator


def login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



class DateInput(forms.DateInput):
    input_type = 'date'

class AuthorisationMixin:

    @method_decorator(login_required())
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

class AuthorisedUpdateView(AuthorisationMixin, UpdateView):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name, context = {'form': self.form_class(instance = request.user)})

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST or None, request.FILES, instance = request.user)
        if form.is_valid():
            return self.form_valid(form)
        return redirect(self.get_success_url())
    
    def get_success_url(self) -> str:
        return reverse(self.success_url, host='auth')
    
class UnauthorisedFormView(FormView):

    http_method_names = ['get', 'post']

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated and not getattr(self, 'login_url', False):
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form, request)
    
    def form_valid(self, form: Any, request: HttpRequest) -> HttpResponse:
        return render(request, template_name = self.template_name, context = {'form': form})

    def form_invalid(self, form: Any, request: HttpRequest) -> HttpResponse:
        return render(request, template_name = self.template_name, context = {'form': form})

class AuthorisedFormView(AuthorisationMixin, FormView):
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated and not getattr(self, 'login_url', False):
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form, request)
    
    def form_valid(self, form: Any, request: HttpRequest) -> HttpResponse:
        return render(request, template_name = self.template_name, context = {'form': form})

    def form_invalid(self, form: Any, request: HttpRequest) -> HttpResponse:
        return render(request, template_name = self.template_name, context = {'form': form})
    
class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, text_content, recipient_list, sender):
        self.subject = subject
        self.recipient_list = recipient_list
        self.text_content = text_content
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.text_content, self.sender, self.recipient_list, html_message=self.html_content)
