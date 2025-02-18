from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('departments', views.departments, name='departments'),
    path('doctors', views.doctors, name='doctors'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),
    path('webappointment', views.webAppointment, name='webappointment'),
    path('tos', views.tos, name='tos'),
    path('privacy', views.privacy, name='privacy'),
]