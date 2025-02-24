from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('appointment_list/', views.appointmentList, name='appointment_list'),
    path('appointment_list/all', views.all_appointment_list, name='all_appointment_list'),
    path('specialities/', views.specialities, name='specialities'),
    path('users/', views.users, name='users'),
    path('users/<int:pk>', views.users_profile, name='users_profile'),
    path('doctors/', views.doctors, name='doctors_list'),
    path('doctors/<int:doctor_id>/schedule/', views.schedule_view, name='schedule_view'),
    # path('book_slot/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('doctors/createschedule/', views.createschedule, name='createschedule'),
    path('staff/', views.staff, name='staff_list'),
    path('patients/', views.patients, name='patients_list'),
    path('transaction/', views.transaction, name='transaction'),
    path('login/', views.adminLogin, name='admin_login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activation_sent/', lambda request: render(request, 'administration/activation_sent.html'), name='activation_sent'),
    path('activation_invalid/', lambda request: render(request, 'administration/activation_invalid.html'), name='activation_invalid'),
]