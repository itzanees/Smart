from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminHome, name='admin_home'),
    path('profile/', views.adminProfile, name='admin_profile'),
    path('appointment_list/', views.appointmentList, name='appointment_list'),
    path('specialities/', views.specialities, name='specialities'),
    path('doctors/', views.doctors, name='doctors'),
    path('patients/', views.patients, name='patients'),
    path('transaction/', views.transaction, name='transaction'),

]