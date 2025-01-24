from django.urls import path
from . import views


urlpatterns = [
    path('', views.doctorHome, name='doctor_dashboard'),
    path('profile/', views.doctorProfile, name='doctor_profile'),
    path('appointment_list/', views.drAppointmentList, name='doctor_appointment_list'),
    path('patients/', views.patients, name='doctor_patients_list'),
    path('schedule/', views.schedules, name='doctor_schedule'),
    path('login/', views.doctorLogin, name='doctor_login'),
    path('forgot_password/', views.doctorForgotPassword, name='doctor_forgot_password'),

     path('calendar/', views.schedules, name='calendar'),  # Base calendar view
    path('calendar/<int:year>/<int:month>/', views.schedules, name='calendar_with_date'),  # With year/month
]