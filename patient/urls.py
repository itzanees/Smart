from django.urls import path
from . import views


urlpatterns = [
    path('', views.patientHome, name='patient_dashboard'),
    # path('profile/', views.adminProfile, name='admin_profile'),
    # path('appointment_list/', views.appointmentList, name='appointment_list'),
    # path('specialities/', views.specialities, name='specialities'),
    # path('doctors/', views.doctors, name='doctors_list'),
    # path('patients/', views.patients, name='patients_list'),
    # path('transaction/', views.transaction, name='transaction'),
    # path('login/', views.adminLogin, name='admin_login'),
    # path('forgot_password/', views.adminForgotPassword, name='admin_forgot_password'),
]