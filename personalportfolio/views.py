from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.views import generic
from django.views.generic import CreateView,ListView
from django.conf import settings
from .mixins import Directions
# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'home.html'
    context_object_name = 'homes'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home = Home.objects.all()
        about = About.objects.all()
        skills= Skills.objects.all()
        certificates = Certificate.objects.filter(is_active=True)
        blogs = Blog.objects.filter(is_active=True)
        portfolio = PortfolioProjects.objects.filter(is_active=True)
        contact = Contact.objects.all()

        context['certificates'] = certificates
        context['blogs'] = blogs
        context['portfolios'] = portfolio
        context['about'] = about
        context['home'] = home
        context['skills'] = skills
        context['contact'] = contact
        return context
    def post(self, request, *args, **kwargs):
        form=ContactForm()
        if form.is_valid():
            form.save()
            return redirect("homepage")
        else:
            form = ContactForm()
        return render(request, 'home.html', {'form':form})


    def post(self, request, *args, **kwargs):
        form = CvFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("homepage")
        else:
            form = CvFileForm()
        return render(request, 'home.html', {'form': form})

    def form_valid(self, form):
        form.instance.created_by = self.request
        form.save()
        messages.success(self.request, "Success! Thank you for contacting me. I'll get back to you as soon as possible")
        return super().form_valid(form)
    def route(self, request):
        context = {"google_api_key": settings.GOOGLE_API_KEY}
        return render(request, 'main/route.html', context)

    def map(request):

        lat_a = request.GET.get("lat_a")
        long_a = request.GET.get("long_a")
        lat_b = request.GET.get("lat_b")
        long_b = request.GET.get("long_b")
        directions = Directions(
            lat_a=lat_a,
            long_a=long_a,
            lat_b=lat_b,
            long_b=long_b
        )

        context = {
            "google_api_key": settings.GOOGLE_API_KEY,
            "lat_a": lat_a,
            "long_a": long_a,
            "lat_b": lat_b,
            "long_b": long_b,
            "origin": f'{lat_a}, {long_a}',
            "destination": f'{lat_b}, {long_b}',
            "directions": directions,

        }
        return render(request, 'main/map.html', context)



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

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context["certificates"] = Certificate.objects.all()
        #return context

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
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, "Success! Thank you for contacting me. I'll get back to you as soon as possible")
        return super().form_valid(form)
