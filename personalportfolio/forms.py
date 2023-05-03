from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    name = forms.CharField( required=True, max_length=100,
                widget=forms.TextInput(attrs={
        'placeholder': 'Your name',
        'type': 'text',
        'name': 'name',
        'class': 'form-control',
    }))
    email= forms.EmailField( required=True,
            widget=forms.TextInput(attrs={
        'placeholder': 'Enter your Email',
        'type': 'text',
        'name': 'email',
        'class': 'form-control',
    }))
    subject= forms.CharField( max_length=100,
                widget=forms.TextInput(attrs={
        'placeholder': 'Subject matter',
        'type': 'text',
        'name': 'subject',
        'class': 'form-control',
    }))
    message=forms.CharField( required=True,
        widget=forms.Textarea(attrs={
        'placeholder': 'Enter your message',
        'type': 'text',
        'name': 'messages',
        'rows': 7,
    }))
    class Meta:
        model = PortfolioProfile
        fields = ('name', 'email', 'subject', 'message')
class CvFileForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ('resume',)
 class SkillsImageForm(forms.ModelForm):
    class Meta:
        model=Skills
        fields =('image',)
        
 class PortfolioImageForm(forms.ModelForm):
   class Meta:
       model = PortfolioProjects
       fields = ('snap', )       
 class MeasurementModelForm(forms.ModelForm):
    model = Measurement
    fields = ('destination', )      
