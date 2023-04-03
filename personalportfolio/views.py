from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.views import generic
from django.views.generic import CreateView,ListView
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
        context['portfolios'] = portfolio
        context['about'] = about
        context['home'] = home
        context['skills'] = skills
        return context

    def post(self, request, *args, **kwargs):
        form = CvFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("homepage")
        else:
            form = CvFileForm()
        return render(request, 'home.html', {'form': form})


class AboutView(generic.ListView):
    model = About
    template_name = 'about.html'
    context_object_name = 'about'

class SkillsView(CreateView):
    model = Skills
    form_class = SkillsImageForm
    template_name = 'skills.html'
    context_object_name = "skills"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skills.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = SkillsImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("homepage")
        else:
            form = SkillsImageForm()
        return render(request, 'skills.html', {'form': form})


class BlogView(generic.ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blogdetail.html'
    context_object_name = 'blogs'

class CertificateView(generic.ListView):
    model = Certificate
    template_name = 'certificate.html'
    paginate_by = 4
    context_object_name = 'certificates'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class PortfolioView(generic.ListView):
    model = PortfolioProjects
    template_name = 'portfolio.html'
    context_object_name = 'portfolios'
    form_class = PortfolioImageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolios'] = PortfolioProjects.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = PortfolioImageForm(request.POST, request.files)
        if form.is_valid():
            form.save()
            return redirect("homepage")
        else:
           form = PortfolioImageForm()
        return render(request, 'portfolio.html', {'form': form})


    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class PortfolioDetailView(generic.DetailView):
    model = PortfolioProjects
    template_name = 'portfoliodetail.html'
    context_object_name = 'portfolios'

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

