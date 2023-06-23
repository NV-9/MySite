# ABC View Templates
# 2 branches: unauthorised and authorised

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse 
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, UpdateView
import threading
from typing import Any

class AuthorisationMixin:
    login_url = settings.LOGIN_URL

    @method_decorator(login_required(login_url=login_url))
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

class AuthorisedUpdateView(AuthorisationMixin, UpdateView):
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name, context = {'form': self.form_class(instance = request.user)})

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST or None, request.FILES, instance = request.user)
        if form.is_valid():
            return self.form_valid(form)
        return redirect(self.get_success_url())
    
    def get_success_url(self) -> str:
        return reverse(self.success_url)
    
class UnauthorisedFormView(FormView):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
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

class AuthorisedFormView(AuthorisationMixin, UnauthorisedFormView):
    pass
    
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
        

