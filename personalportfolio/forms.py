from django import forms

class ContactForm(forms.Form):
    name = forms.CharField( widget=forms.TextInput(attrs={
        'placeholder': 'Your name',
        'type': 'text',
        'name': 'name',
        'class': 'form-control',
    }))
    email= forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your Email',
        'type': 'text',
        'name': 'email',
        'class': 'form-control',
    }))
    subject= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Subject matter',
        'type': 'text',
        'name': 'subject',
        'class': 'form-control',
    }))
    message=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your message',
        'type': 'text',
        'name': 'messages',
        'class': 'form-control',
    }))
