from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('skills/', views.SkillsView.as_view(), name='skills'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('portfolio/<int:pk>', views.PortfolioDetailView.as_view(), name='portfoliodetail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('blog/', views.BlogView.as_view(), name="blog"),
    path('blog/<slug:slug>', views.BlogDetailView.as_view(), name='blogdetail'),
    path('certificate/', views.CertificateView.as_view(), name='certificate'),

]
