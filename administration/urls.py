from django.urls import path
from . import views


urlpatterns = [
    path('', views.adminHome, name='admin_home'),
    path('profile/', views.adminProfile, name='admin_profile'),
    path('appointment_list/', views.appointmentList, name='appointment_list'),
    path('specialities/', views.specialities, name='specialities'),
    # path('specialities/create/', views.createDep, name='create_department'),
    # path('specialities/update/', views.updateDep, name='update_department'),
    path('users/', views.users, name='users'),
    path('users/<int:pk>', views.usersProfile, name='users_profile'),
    path('doctors/', views.doctors, name='doctors_list'),
    path('doctors/<int:doctor_id>/schedule/', views.schedule_view, name='schedule_view'),
    path('book_slot/<int:slot_id>/', views.book_slot, name='book_slot'),
    # path('doctors/<int:pk>', views.doctorDetails, name='doctor_profile'),
    path('staff/', views.staff, name='staff_list'),
    path('patients/', views.patients, name='patients_list'),
    # path('patients/<int:pk>', views.patientsProfile, name='patients_profile'),
    path('transaction/', views.transaction, name='transaction'),
    path('login/', views.adminLogin, name='admin_login'),
    # path('forgot_password/', views.adminForgotPassword, name='admin_forgot_password'),
    path('logout/', views.Logout, name='logout'),

]