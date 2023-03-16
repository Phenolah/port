from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('success', views.successView, name='success'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
