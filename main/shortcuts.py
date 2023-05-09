from django.views import View
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

class LoginRequiredMixin:
    login_url = settings.LOGIN_URL or '../../login'

    @method_decorator(login_required(login_url=login_url))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self, request, *args, **kwargs)



class BaseView(View):
    template_name = None
    context = {}

    def dispatch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


class AuthorisedView(BaseView, LoginRequiredMixin):
    '''
    AuthorisedView
    --------------
    template_name  - path to template file 
    context  - variable dictionary passed into the template
    login_url  - determined by `LOGIN_URL` variable in settings! Defaults to '../../login' of site!
    '''
    login_url = settings.LOGIN_URL or '../../login'
    template_name = None
    context = {}
    
    def get(self, request, *args, **kwargs):
        self.add_context(request, *args, **kwargs)
        return render(request, self.template_name, self.context)

    # Allows updating context directly
    def add_context(self, request, *args, **kwargs):
        return self.context.update({})


class FormView(View):
    '''
    FormView
    --------
    template_name  - path to template file 
    context  - variable dictionary passed into the template
    form_class  - sets the form to be sent in view
    error_message  - message to be shown if post data is invalid
    success_url  - redirect url if form is valid
    '''
    template_name = None
    context = {}
    form_class = None
    error_message = None
    sucess_url = None

    # Unloading method for separating request methods
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET': return self.get(request, *args, **kwargs)
        elif request.method == 'POST': return self.post(request, *args, **kwargs)

    # Main get method for serving webpage
    def get(self, request, *args, **kwargs):
        self.add_context(request, *args, **kwargs)
        return render(request, self.template_name, self.context)
    
    # Main post method for handing form data
    def post(self, request, *args, **kwargs):
        # adding in post data to form
        form = self.form_class(request.POST, request.FILES or None)
        # validating and cleaning form
        if form.is_valid():
            # saving form
            form.save()
            # redirecting if present
            if self.success_url is not None: 
                return HttpResponseRedirect(self.sucess_url)
            return self.get()
        else:
            # adding in error message to context data
            self.add_context({'error': self.error_message})
            return self.get()

    # Allows updating context directly
    def add_context(self, request, *args, **kwargs):
        return self.context.update({
            'form': self.form_class()
        })


class AuthorisedFormView(FormView, LoginRequiredMixin):
    '''
    FormView
    --------
    template_name  - path to template file 
    context  - variable dictionary passed into the template
    form_class  - sets the form to be sent in view
    error_message  - message to be shown if post data is invalid
    success_url  - redirect url if form is valid
    login_url  - determined by `LOGIN_URL` variable in settings! Defaults to '../../login' of site!
    '''
    login_url = settings.LOGIN_URL or '../../login'

    @method_decorator(login_required(login_url=login_url)) # Decorating with login reuqired 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
class MultiFormView(View):
    '''
    MultiFormView
    -------------
    template_name  - path to template file 
    context  - variable dictionary passed into the template
    forms  - all forms to be sent + mapped respones (as callables)
    error_message  - message to be shown if post data is invalid
    success_url  - redirect url if form is valid
    login_url  - determined by `LOGIN_URL` variable in settings! Defaults to '../../login' of site!
    Forms - Usage
    {
        Form : {
            'name' : 'context_variable_name',
            'button' : 'post_button_name',
            'action' : callable_function
        }
    }
    '''
    template_name = None
    context = {}
    forms = {}
    error_message = None
    sucess_url = None
    login_url = settings.LOGIN_URL or '../../login'

    # Unloading method for separating request methods
    
    @method_decorator(login_required(login_url=login_url))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET': return self.get(request, *args, **kwargs)
        elif request.method == 'POST': return self.post(request, *args, **kwargs)

    # Main get method for serving webpage
    def get(self, request, *args, **kwargs):
        self.add_context(request, *args, **kwargs)   
        return render(request, self.template_name, self.context)
    
    # Allows updating context directly
    def add_context(self, request, *args, **kwargs):
        for form in self.forms: 
            self.context[self.forms[form]['name']] = form()
        return self.context

    # Main post method for handing form data
    def post(self, request, *args, **kwargs):
        # Selecting form and passing in post data - Only uses 1 form at a time
        form = None
        for form in self.forms:
            if self.forms[form]['button'] in request.POST:
                form = form 
                break
        if not form:
            return self.get(request, *args, **kwargs)
       
        request_form = form(request.POST, request.FILES or None)
        # status represents validity of form, response is None if status is True
        status, response = self.forms[form]['action'](request, request_form)
        if not status:  
            self.context[response[0]] = response[1]
        elif response:
            
            return HttpResponseRedirect(response)
        return self.get(request, *args, **kwargs)