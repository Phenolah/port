from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from django.views.generic.list import ListView
from django.contrib import messages
from django.views import generic
# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'home.html'
    context_object_name = 'homes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home = Home.objects.all()
        about = About.objects.all()
        skills= Skills.objects.all()
        certificates = Certificate.objects.filter(is_active=True)
        blogs = Blog.objects.filter(is_active=True)
        portfolio = PortfolioProjects.objects.filter(is_active=True)

        context['certificates'] = certificates
        context['blogs'] = blogs
        context['portfolio'] = portfolio
        context['about'] = about
        context['home'] = home
        context['skills'] = skills
        return context

    def upload_file(self, request):
        if request.method == 'POST':
            form = CvFileForm(request.POST,request.FILES)
            if form.is_valid():
                cv_upload = CvFileForm(request.FILES['cv'])
                cv_upload.save()
                return redirect('homepage')
            else:
                form = CvFileForm()
            return render(request, 'home.html', {'form': form })


class AboutView(generic.ListView):
    model = About
    template_name = 'about.html'
    context_object_name = 'about'

class SkillsView(generic.ListView):
    model = Skills
    template_name = 'skills.html'
    context_object_name = "skills"
    def upload_image(self, request):
        if request.method == 'POST':
            form = SkillsImageForm(request.POST,request.FILES)
            if form.is_valid():
                skills_photo = Skills()
                skills_photo.save()
            else:
                form = SkillsImageForm()
            return render(request, 'skills.html', {'form': form})

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

class ContactView(generic.FormView):
    success_url = "home"
    def get(self, *args, **kwargs):
        form = ContactForm(self.request.POST)
        context = {
            'form': form,
        }
        return render(self.request, 'contact.html', context)
    def form_valid(self, form):
        form = ContactForm(self.request.POST)
        form.save()
        messages.success(self.request, "Success! Thank you for contacting me. I'll get back to you as soon as possible")
        return super().form_valid(form)

