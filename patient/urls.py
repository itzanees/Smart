from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.patientHome, name='patient_dashboard'),
    # path('login/', views.patientLogin, name='patient_login'),
     path('login/', views.patientLogin, name='patient_login'),
    path('registration/', views.patientRegistration, name='patient_registration'),
    path('profile/', views.patientProfile, name='patient_profile'),
    path('appointment/', views.appointment, name='appointment'),
    # path('bookings/', views.bookings, name='bookings'),
    path('services/', views.services, name='hosp_services'),
    path('specialities/', views.specialities, name='hosp_specialities'),
    path('doctors/', views.doctors, name='hos_doctors_list'),
    path('transaction/', views.transaction, name='pat_transaction'),
    path('forgot_password/', views.patForgotPassword, name='pat_forgot_password'),
]