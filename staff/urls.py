from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path('', views.staff_dashboard, name='staff_dashboard'),
    path('login/', views.staffLogin, name='staff_login'),
    path('profile/', views.staff_profile, name='staff_profile'),
    path('change_password/', views.staff_change_password, name='staff_change_password'),
    path("password_change_done/", PasswordChangeDoneView.as_view(template_name="staff/password_change_done.html"), name="staff_password_change_done"),
    path('appointment_list/', views.staff_appointment_list, name='staff_appointment_list'),
    path('specialities/', views.staff_specialities, name='staff_specialities'),
    path('doctors/', views.staff_doctors, name='staff_doctors'),
    path('doctors/<int:doctor_id>/schedule/', views.st_schedule_view, name='st_schedule_view'),
    path('patients/', views.staff_patients, name='staff_patients'),
    path('transaction/', views.staff_transaction, name='staff_transaction'),
    path('search/', views.staff_search, name='staff_search')
]