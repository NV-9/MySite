from django import forms 
from .models import ContactMessages


class ContactForm(forms.ModelForm):

    name = forms.CharField(
        max_length = 50, 
        required = True, 
        label = 'Your Name',
        widget = forms.TextInput(attrs = {'class': 'form-control', 'id': 'name'})
    )
    email = forms.EmailField(
        required = True, 
        label = 'Your Email',
        widget = forms.EmailInput(attrs = {'class': 'form-control', 'id': 'email'})
    )
    subject = forms.CharField(
        max_length = 100, 
        required = True,
        label = 'Subject',
        widget = forms.TextInput(attrs = {'class': 'form-control', 'id': 'subject'})
    )
    content = forms.CharField(
        max_length = 2000, 
        required = True,
        label = 'Message',
        widget = forms.Textarea(attrs = {'class': 'form-control', 'id': 'content', 'rows': '10'})
    )

    class Meta:
        model = ContactMessages
        fields = ('name', 'email', 'subject', 'content',)
    
    def save(self, commit: bool = True, ip = None):
        instance = super().save(False)
        if ip:
            instance.ip = ip 
            instance.save(commit)
        return instance 
