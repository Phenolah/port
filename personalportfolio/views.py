from django.shortcuts import render, HttpResponse
from .forms import *
# Create your views here.

def home(request):
    form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'home.html', context)
