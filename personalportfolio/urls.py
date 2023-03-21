from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('portfolio/', views.PortfolioDetailView.as_view(), name='portfolio'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('blog/', views.blog, name="blog"),
    path('blog/', views.BlogDetailView.as_view(), name='blogdetail'),
    path('certificate/', views.Certificate, name='certificate')
]
