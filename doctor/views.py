from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from administration.models import Doctor, Patient, Staff, Schedule, Appointment, Department, MedicalRecord, Billing, CustomUser
from . forms import DoctorLoginForm, MedicalRecordForm, DoctorPasswordResetRequestForm
from administration.forms import CustomPasswordChangeForm, ProfileUpdateForm
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from administration.models import Schedule
from django.db.models import Q

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

@login_required(login_url='doctor_login')
def doctor_change_password(request):
    user = request.user
    if user is not None and user.user_type == 'Doctor':
        if request.method == "POST":
            form = CustomPasswordChangeForm(user = request.user, data = request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user) 
                messages.success(request, "Password Changed Successfully")
                return redirect("doctor_change_password")
            else:
                messages.error(request, "Please try again.")
                return redirect("doctor_change_password")
        else:
            form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'doctor/change-password.html', {'form':form})
    else:
        if request.user.is_superuser:
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

def doctor_forgot_password(request):
    form = DoctorPasswordResetRequestForm()
    if request.method =='POST':
        form = DoctorPasswordResetRequestForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.password_request = True
            doc.save()
            messages.success(request, "Passaword reset request sent.")
            return redirect('doctor_forgot_password')
        else:
            messages.error(request, "User not found.")
            return redirect('doctor_forgot_password')
    return render(request, 'doctor/doctor-change-password.html', {'form':form})

@login_required(login_url='doctor_login')
def doctor_dashboard(request):
    if request.user.is_superuser:
        return render(request, 'doctor/doctor-dashboard.html')
    
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(user=user)
    today = timezone.now()
    appointments_prev = Appointment.objects.filter(doctor=doctor, appointment_on__date__lt=today)
    appointments = Appointment.objects.filter(doctor=doctor, appointment_on__date__gt=today)
    appointments_today = Appointment.objects.filter(doctor=doctor, appointment_on__date=today)
    if doctor.profile_updated:
        return render(request, 'doctor/doctor-dashboard.html', {'doctor': doctor, 'appointments':appointments, 'appointments_today':appointments_today, 'appointments_prev':appointments_prev})
    else:
        messages.warning(request,"Please Update your profile!!")
        return redirect('doctor_profile')

@login_required(login_url='doctor_login')
def doctor_profile(request):
    user = get_object_or_404(get_user_model(), id=request.user.id)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user, user=user)
        if form.is_valid():
            form.save()
            doctor, created = Doctor.objects.get_or_create(user=user)
            doctor.profile_updated = True
            doctor.save()
            messages.success(request, f"Dr. {user.username}'s profile updated.")
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
    today = timezone.now()
    available_slots = Schedule.objects.filter(doctor=doctor, date__gte=today).order_by("date")
    av_slot_paginator = Paginator(available_slots, 8)
    av_slot_page_num = request.GET.get('page')
    av_slot_page_obj = av_slot_paginator.get_page(av_slot_page_num)
    context = {
        'doctor':doctor,
        'schedules':av_slot_page_obj,
    }
    
    return render(request, 'doctor/schedule.html', context)

@login_required(login_url='doctor_login')
def doctor_appointment_list(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(user=user)
    today = timezone.now()
    appointments = Appointment.objects.filter(doctor=doctor, appointment_on__date=today.date())
    return render(request, 'doctor/appointments.html', {'doctor':doctor, 'appointments':appointments})

@login_required(login_url='doctor_login')
def patients(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(user=user)
    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()
    return render(request, 'doctor/my-patients.html', {'doctor':doctor, 'patients':patients})

@login_required(login_url='doctor_login')
def doc_pat_profile(request, pk):
    pat = Patient.objects.get(id=pk)
    appointment = Appointment.objects.filter(patient=pat).order_by('-appointment_on__date')
    appointment_paginator = Paginator(appointment, 5)
    appointment_page_num = request.GET.get('page')
    appointment_page_obj = appointment_paginator.get_page(appointment_page_num)
    today = timezone.now()
    context = {
        'today':today.date(),
        'patient':pat,
        'appointments':appointment_page_obj,
    }
    return render(request, 'doctor/patient-profile.html', context)

@login_required(login_url='doctor_login')
def doc_pat_records(request, pk, app_no):
    patient_user = get_object_or_404(get_user_model(), id=pk)
    patient = get_object_or_404(Patient, user=patient_user)
    appointment = get_object_or_404(Appointment, appointment_number=app_no)
    
    record, created = MedicalRecord.objects.get_or_create(appointment=appointment, defaults={
        # 'patient': patient,
        # 'doctor': Doctor.objects.get(user=request.user),
        # 'department': Department.objects.get(doctor=Doctor.objects.get(user=request.user)),
        'is_opened': True
    })
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.is_opened = True
           
            closed = request.POST.get('is_closed')
            record.is_closed = True if closed == 'on' else False
            print(appointment.status)
            appointment.status = 'CO'
            next_appointment = form.cleaned_data.get('next_appointment')
            if next_appointment:
                appointment.follow_up = next_appointment
            appointment.save()
            record.save()
            messages.success(request, "Record Saved Successfully.")
            return redirect('doc_pat_records', pk=pk, app_no=app_no)
        else:
            messages.error(request, "Failed to Save Record.")

    form = MedicalRecordForm(instance=record)
    if appointment.follow_up:
        form.fields['next_appointment'].initial = appointment.follow_up
    context = {
        'form': form,
        'pat': patient,
        'app': appointment,
        'record': record
    }

    condition = False
    if record.is_closed:
        condition = True

    if condition:
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
    return render(request, 'doctor/medical-records.html', context)

@login_required(login_url='doctor_login')
def doc_pat_search(request):
    query = request.GET.get('q', '')
    results = {
        'patients':[],
        'appointments':[],
        }

    if query:
        patients = Patient.objects.filter(Q(user__username__icontains = query))
        appointments = Appointment.objects.filter(Q(patient__user__username__icontains=query))

        results['patients'] = patients
        results['appointments'] = appointments


    return render(request, 'doctor/search_result.html', {'results': results, 'query': query})