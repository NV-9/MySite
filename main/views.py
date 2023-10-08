from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic.edit import FormView
from typing import Any

from .forms import ContactForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class HomeView(FormView):
    template_name = 'main/home.html'
    form_class = ContactForm
    extra_context = settings.CUSTOM_DATA

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form, request)

    def form_invalid(self, form: Any, request: HttpRequest) -> HttpResponse:
        return JsonResponse({'success': False})
    
    def form_valid(self, form: Any, request: HttpRequest) -> HttpResponse:
        form.save(ip = get_client_ip(request))  
        return JsonResponse({'success': True})

