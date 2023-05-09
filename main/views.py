from django.http import JsonResponse
from .shortcuts import FormView, BaseView
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
    context = {
        'linkedin': 'https://www.linkedin.com/in/viswamedha-nalabotu-056852189/',
        'github': 'https://github.com/NV-9',
        'instagram': 'https://instagram.com/nalabotuviswamedha',
    }

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save(ip = get_client_ip(request))  
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

from django.shortcuts import render

class PrivacyView(BaseView):
    template_name = 'main/privacy.html'

