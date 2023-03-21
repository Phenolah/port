from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from django.views.generic.list import ListView
from django.core.mail import send_mail, BadHeaderError
# Create your views here.

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request,'about.html')

def skills(request):
    return render(request, 'skills.html')

def blog(request):
    return render(request, 'blog.html')

class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blogdetail.html'

class CertificateView(generic.ListView):
    model = Certificate
    template_name = 'certificate.html'
    paginate_by = 4
class PortfolioView(generic.ListView):
    model = PortfolioProjects
    template_name = 'portfolio.html'
    paginate_by = 10

class PortfolioDetailView(generic.DetailView):
    model = PortfolioProjects
    template_name = 'portfoliodetail.html'
class ContactView(ListView):
    context_object_name = 'skills'
    def get(self, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(self.request, 'contact.html', context)
    def get(self, *args, **kwargs):
        form = ContactForm()
        context={
            'form': form
        }
        if self.request.method == "POST":
            form = ContactForm(self.request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                sender = form.cleaned_data['email']
                recipients = ['phenolaha@gmail.com']
                try:
                    send_mail(name, subject, message, sender, recipients)
                    form.save()
                except BadHeaderError:
                    return HttpResponse("Invalid header found ")
                return redirect('success')
                context = {'success': True}
        return render(self.request, 'contact.html', context)


def successView(request):
    return HttpResponse (request, "Success! Thank your for your message. I will get back to you as soon as possible:)")

