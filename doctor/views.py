from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from administration.models import Doctor, Patient, Staff, Schedule, Appointment, Department, MedicalRecord, Billing, CustomUser
from . forms import DoctorLoginForm, MedicalRecordForm
from administration.forms import CustomPasswordChangeForm, ProfileUpdateForm
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
import calendar
from django.core.paginator import Paginator
from administration.models import Schedule

def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username= username, password=password)
            if user is not None and user.user_type == 'Doctor' or user.is_superuser:
                login(request, user)
                return redirect('doctor_dashboard')
    else:
        form = DoctorLoginForm()
    return render(request, 'doctor/login.html', {'form':form})

@login_required(login_url='staff_login')
def doctor_change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect("doctor_change_password")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'doctor/change-password.html', {'form':form})

def doctorForgotPassword(request):
    return render(request, 'doctor/doctor-change-password.html')

@login_required(login_url='doctor_login')
def doctor_dashboard(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(user=user)
    today = timezone.now()
    appointments = Appointment.objects.filter(doctor=doctor, appointment_on__date__gt=today)
    appointments_today = Appointment.objects.filter(doctor=doctor, appointment_on__date=today)
    return render(request, 'doctor/doctor-dashboard.html', {'doctor': doctor, 'appointments':appointments, 'appointments_today':appointments_today})

@login_required(login_url='doctor_login')
def doctor_profile(request):
    user = get_object_or_404(get_user_model(), id=request.user.id)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.username}'s profile updated")
            return redirect('doctor_profile')
        else:
            messages.error(request,"Profile is not uptaded!!!")
            return redirect('doctor_profile')


    profileform = ProfileUpdateForm(user=user, instance=user)
    doctor = Doctor.objects.get(user=user)
    return render(request, 'doctor/doctor-profile-settings.html', {'doctor':doctor, 'profileform':profileform, 'user':user})

@login_required(login_url='doctor_login')
def schedules(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(user=user)
   
    available_slots = Schedule.objects.filter(doctor=doctor).order_by("date")
    av_slot_paginator = Paginator(available_slots, 8)
    av_slot_page_num = request.GET.get('page')
    av_slot_page_obj = av_slot_paginator.get_page(av_slot_page_num)
    context = {
        'doctor':doctor,
        'schedules':av_slot_page_obj,
    }
    
    return render(request, 'doctor/schedule.html', context)

def doctor_appointment_list(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(user=user)
    today = timezone.now()
    appointments = Appointment.objects.filter(doctor=doctor, appointment_on__date__gte=today)
    return render(request, 'doctor/appointments.html', {'doctor':doctor, 'appointments':appointments})


def patients(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(user=user)
    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()
    return render(request, 'doctor/my-patients.html', {'doctor':doctor, 'patients':patients})

def doc_pat_profile(request, pk):
    pat = Patient.objects.get(id=pk)
    appointment = Appointment.objects.filter(patient=pat)

    context = {
        'patient':pat,
        'appointments':appointment,
    }
    return render(request, 'doctor/patient-profile.html', context)

# def doc_pat_prescription(request, pk):
#     # patient = Patient.objects.get(id=pk)
#     appointment = Appointment.objects.get(id=pk)
#     med_record =  MedicalRecord.objects.get( appointment=appointment )
#     # med_record =  MedicalRecord.objects.get(appointment_number = appointment_number)
#     if med_record:
#         print("Found med")
#     else:
#         print("Nothing")
#     context = {
#         'med_record':med_record,
#         'appointment':appointment,
#         # 'patient':patient,
#     }
#     return render(request, 'doctor/edit-prescription.html', context)

    # schedule_id = int(path.split('/')[4])

def doc_pat_records(request, patient_slug):
    print(patient_slug)
    pat = get_object_or_404(get_user_model(), id=2)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            doctor = get_object_or_404(get_user_model(), id=request.user.id)
            # user = get_object_or_404(CustomUser, id=user_id)
            dep = doctor.department
            

            form.save()

    form = MedicalRecordForm(user=pat, instance=pat)
    context ={
        'form':form,
        'pat':pat,
        }

    return render(request, 'doctor/medical-records.html', context)