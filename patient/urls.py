from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeDoneView


urlpatterns = [
    path('', views.patient_dashboard, name='patient_dashboard'),
    path('login/', views.patient_login, name='patient_login'),
    path('registration/', views.patient_registration, name='patient_registration'),
    path('forgot_password/', views.pat_forgot_password, name='pat_forgot_password'),
    path('change_password/', views.pat_change_password, name='pat_change_password'),
    path("password_change_done/", PasswordChangeDoneView.as_view(template_name="password_change_done.html"), name="password_change_done"),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('lookup/', views.doc_search, name = 'doc_search'),
    path('search/', views.pat_search, name= 'pat_search'),
    path('appointment/doc/<int:pk>', views.appointment_doc, name='appointment_doc'),
    path('book_slot/<int:slot_id>/', views.pat_book_slot, name='pat_book_slot'),
    path('book_slot/successful/', views.pat_book_success, name='pat_book_success'),
    path('specialities/', views.hosp_specialities, name='hosp_specialities'),
    path('specialities/<int:pk>', views.doc_hosp_specialities, name='doc_hosp_specialities'),
    path('doctors/<int:pk>', views.pat_doctor_profile, name='pat_doctor_profile'),
    path('doctors/<int:doctor_id>/schedule/', views.pat_schedule_view, name='pat_schedule_view'),
    path('bill/', views.view_pat_bill, name='view_pat_bill'),
]