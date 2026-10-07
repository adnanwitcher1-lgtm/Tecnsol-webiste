from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about'),
    path('services/', views.services_page, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('services/<slug:slug>/download/', views.service_download, name='service_download'),
    path('projects/', views.projects_page, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('tech-stack/', views.tech_stack_page, name='tech_stack'),
    path('testimonials/', views.testimonials_page, name='testimonials'),
    path('contact/', views.contact_page, name='contact'),
]
