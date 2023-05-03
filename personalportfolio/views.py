from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.views import generic
from django.views.generic import CreateView, ListView
from django.conf import settings
from .mixins import Directions
from django.urls import reverse_lazy
from geopy.geocoders import Nominatim
from .utils import *
from django.contrib.gis.geoip2 import GeoIP2
import folium
from geopy.distance import geodesic

# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'home.html'
    context_object_name = 'homes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home = Home.objects.all()
        about = About.objects.all()
        skills = Skills.objects.all()
        certificates = Certificate.objects.filter(is_active=True)
        blogs = Blog.objects.filter(is_active=True)
        portfolio = PortfolioProjects.objects.filter(is_active=True)
        contact = Contact.objects.all()

        context['certificates'] = certificates
        context['blogs'] = blogs
        context['portfolios'] = portfolio
        context['about'] = about
        context['homes'] = home
        context['skills'] = skills
        context['contact'] = contact
        return context

    def post(self, request, *args, **kwargs):
        print('HomeView.get_context_data() was called')
        contact_form = ContactForm(request.POST)
        cv_form = CvFileForm(request.POST, request.FILES)
        if contact_form.is_valid():
            # Create a new Contact object with the submitted form data
            contact = Contact(
                name=contact_form.cleaned_data['name'],
                email=contact_form.cleaned_data['email'],
                subject=contact_form.cleaned_data['subject'],
                message=contact_form.cleaned_data['message'],
            )
            contact.save()
            # Add a success message to the user's session
            messages.success(self.request,
                             "Success! Thank you for contacting me. I'll get back to you as soon as possible")
            # Redirect the user to the success page
            return super().form_valid(contact_form)
        elif cv_form.is_valid():
            cv_upload = CvFileForm(request.FILES['resume'])
            cv_upload.save()
            return redirect("homepage")
        else:
            context = self.get_context_data(**kwargs)
            context['contact_form'] = contact_form
            context['cv_form'] = cv_form
            return self.render_to_response(context)

    def form_valid(self, form):
        # Create a new Contact object with the submitted form data
        contact = Contact(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message'],
        )
        contact.save()
        # Add a success message to the user's session
        messages.success(self.request, "Success! Thank you for contacting me. I'll get back to you as soon as possible")
        # Redirect the user to the success page
        return super().form_valid(form)


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

    def get(self, request, *args, **kwargs):
        blogs = get_object_or_404(Blog, pk=kwargs['pk'])
        context = {'blogs': blogs}
        return render(request, 'portfoliodetail.html', context)


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
        context['portfolios'] = PortfolioProjects.objects.filter(is_active=True)
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

    def get(self, request, *args, **kwargs):
        projects = get_object_or_404(PortfolioProjects, pk=kwargs['pk'])
        context = {'portfolios': projects}
        return render(request, 'portfoliodetail.html', context)


class ContactView(generic.FormView):
    success_url = reverse_lazy("homepage")
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm

    def get_ip_address(request):
        x_forwarded_fro = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_fro:
            ip = x_forwarded_fro.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        distance = None
        destination = None
        obj = get_object_or_404(Measurement, id=1)
        measurement_form = MeasurementModelForm(self.request.POST or None)
        geolocator = Nominatim(user_agent="measurements")

        ip_ = get_ip_address(self.request)
        print(ip_)
        ip = '72.14.207.99'
        country, city, lat, lon = get_geo(ip)
        location = geolocator.geocode(city)
        # location coordinates
        l_lat = lat
        l_lon = lon
        pointA = (l_lat, l_lon)

        # initial folium map
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=100)
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='clock here for more', popup=city['city'],
                      icon=folium.Icon(color="pink")).add_to(m)

        if measurement_form.is_valid():
            instance = measurement_form.save(commit=False)
            destination_ = measurement_form.cleaned_data.get('destination')
            destination = geolocator.geocode(destination_)
            print(destination)
            # distance coordinates
            d_lon = destination.longitude
            d_lat = destination.latitude
            # distance coordinates
            d_lat = destination.latitude
            d_lon = destination.longitude
            pointB = (d_lat, d_lon)

            # distance calculation
            distance = round(geodesic(pointA, pointB).km, 2)
            # initial folium map
            m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon),
                           zoom_start=get_zoom(distance))
            # location marker
            folium.Marker([d_lat, d_lon], tooltip='clock here for more', popup=destination,
                          icon=folium.Icon(color="pink")).add_to(m)
            # location marker
            folium.Marker([l_lat, l_lon], tooltip='clock here for more', popup=city['city'],
                          icon=folium.Icon(color="red", icon='cloud')).add_to(m)

            # draw the line between location and destination
            line = folium.Polyline(location=(pointA, pointB), weight=2, color='white')
            m.add_child(line)
            # folium map modification
            instance.location = "Nairobi"
            instance.distance = 5000.0
            instance.save()

        m = m._repr_html_()

        context['distance'] = distance
        context['m_form'] = measurement_form
        context['map'] = m
        context['destination'] = destination
        return context


    def form_valid(self, form):
        # Create a new Contact object with the submitted form data
        contact = Contact(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message'],
        )
        contact.save()

        # Add a success message to the user's session
        messages.success(self.request, "Success! Thank you for contacting me. I'll get back to you as soon as possible")

        # Redirect the user to the success page
        return super().form_valid(form)
