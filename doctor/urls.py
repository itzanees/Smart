from django.urls import path
from . import views


urlpatterns = [
    path('', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('appointments/', views.doctor_appointment_list, name='doctor_appointment_list'),
    path('patients/', views.patients, name='doctor_patients_list'),
    path('patients/<int:pk>', views.doc_pat_profile, name='doc_pat_profile'),
    # path('patients/prescription/<int:appointment_number>', views.doc_pat_prescription, name='doc_pat_prescription'),
    path('patients/<int:pk>/records', views.doc_pat_records, name='doc_pat_records'),
    path('schedule/', views.schedules, name='doctor_schedule'),
    path('login/', views.doctor_login, name='doctor_login'),
    path('change_password/', views.doctor_change_password, name="doctor_change_password"),
    path('forgot_password/', views.doctorForgotPassword, name='doctor_forgot_password'),
    path('profile/', views.doctor_profile, name='doctor_profile'),

]