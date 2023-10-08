from django import forms 
from .models import ContactMessages


class ContactForm(forms.ModelForm):

    name = forms.CharField(
        max_length = 50, 
        required = True, 
        label = 'Your Name',
        widget = forms.TextInput(attrs = {'class': 'input-name', 'id': 'name', 'placeholder': 'Name'})
    )
    email = forms.EmailField(
        required = True, 
        label = 'Your Email',
        widget = forms.EmailInput(attrs = {'class': 'input-name', 'id': 'email', 'placeholder': 'Email'})
    )
    subject = forms.CharField(
        max_length = 100, 
        required = True,
        label = 'Subject',
        widget = forms.TextInput(attrs = {'class': 'input-subject', 'id': 'subject', 'placeholder': 'Subject'})
    )
    content = forms.CharField(
        max_length = 2000, 
        required = True,
        label = 'Message',
        widget = forms.Textarea(attrs = {'class': 'input-textarea', 'id': 'content', 'rows': '10', 'placeholder': 'Message'})
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
