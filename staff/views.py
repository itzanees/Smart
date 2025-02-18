from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
# from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from administration.models import Appointment, Doctor, Patient, Staff, Schedule, CustomUser, Department
from administration.forms import ProfileUpdateForm
from .forms import CustomLoginForm
from administration.forms import CustomPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from django.utils import timezone
from datetime import datetime, timedelta

def staffLogin(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username= username, password=password)
            if user is not None and user.user_type == 'Staff' or user.is_superuser:
                login(request, user)
                return redirect('staff_dashboard')
            else:
                messages.error(request, "Access Denied!!")
                return redirect('staff_login')
    else:
        form = CustomLoginForm()
    return render(request,'staff/login.html', {'form':form})

@login_required(login_url='staff_login')
def staff_profile(request):
    user = get_object_or_404(get_user_model(), id=request.user.id)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user, user=user)
        if form.is_valid():
            form.save()
            return redirect('users_profile', request.user.id)
    profileform = ProfileUpdateForm(user=user, instance=user)
    return render (request, 'staff/profile.html', {'user':user, 'profileform':profileform})

@login_required(login_url='staff_login')
class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "staff/change-password.html"
    success_url = reverse_lazy("staff_password_change_done")

@login_required(login_url='staff_login')
def staff_change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect("staff_password_change_done")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'staff/change-password.html', {'form':form})

@login_required(login_url='staff_login')
def staff_dashboard(request):
    doctors = Doctor.objects.all()[:4]
    patients = Patient.objects.all()[:4]
    appointments = Appointment.objects.filter(appointment_on__date = (datetime.today()))
    appointments_paginator = Paginator(appointments,8)
    appointments_page_num = request.GET.get('page')
    appointments_pag_obj = appointments_paginator.get_page(appointments_page_num)
    context = {
        'appointments':appointments_pag_obj,
        'doctors':doctors,
        'patients':patients,
    }
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        app = Appointment.objects.get(id=app_id)
        app.status = 'RP'
        app.save()
    return render(request, 'staff/index.html', context)

@login_required(login_url='staff_login')
def staff_doctors(request):
    doctors = Doctor.objects.all()
    doc_paginator = Paginator(doctors,8)
    doc_page_num = request.GET.get('page')
    doc_pag_obj = doc_paginator.get_page(doc_page_num)
    return render(request, 'staff/doctor-list.html', {'doctors':doc_pag_obj})

@login_required(login_url='staff_login')
def staff_patients(request):
    patients = Patient.objects.all()
    pat_paginator = Paginator(patients, 8)
    pat_page_num = request.GET.get('page')
    pat_page_obj = pat_paginator.get_page(pat_page_num)
    if request.method=='POST':
        pat_id = request.POST.get('pat_id')
        pat_id = int(pat_id)
        pat_user = CustomUser.objects.get(id = pat_id)
        modal_class = 'show'
        form = ProfileUpdateForm(instance=pat_user, user=pat_user)
        return render(request, 'staff/patient-list.html', {'patients':patients, 'profileform':form, 'modal':modal_class, 'pat_id':pat_id})
    return render(request, 'staff/patient-list.html', {'patients':pat_page_obj})

@login_required(login_url='staff_login')
def staff_specialities(request):
    specialities = Department.objects.all()
    spec_paginator = Paginator(specialities, 8)
    spec_page_num = request.GET.get('page')
    spec_page_obj = spec_paginator.get_page(spec_page_num)
    return render(request, 'staff/specialities.html', {'specialities':spec_page_obj})

@login_required(login_url='staff_login')
def staff_appointment_list(request):
    appointments = Appointment.objects.filter(appointment_on__date = (datetime.today()))

    patients = Patient.objects.all()
    departments = Department.objects.all()
    doctors = Doctor.objects.all()

    if request.method == "POST":
        date = timezone.now().date()
        start_time = timezone.now().time()
        pat_id = request.POST.get('pat_id')
        doc_id = request.POST.get('doc_id')
        fees = request.POST.get('fees')
        print(pat_id, doc_id, date, start_time, fees)
        doctor = Doctor.objects.get(id=doc_id)
        patient = Patient.objects.get(id=pat_id)
        schedule = Schedule(
                doctor=doctor,
                date=date,
                start_time=start_time,
                duration=15,
                is_booked=True
                )
        schedule.save()
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_on=schedule,
            appointment_fees=fees
        )

        appointment.save()
        messages.success(request, f"Created appointment for {patient.first_name}.")
        return redirect('staff_appointment_list')
    context = {
        'appointments':appointments,
        'patients' : patients,
        'departments' : departments,
        'doctors' : doctors,
    }
    return render(request, 'staff/appointment-list.html', context)

@login_required(login_url='staff_login')
def staff_transaction(request):
    appointments = Appointment.objects.filter(medicalrecord__is_closed=True)
    return render(request, 'staff/transactions-list.html', {'appointments': appointments})

@login_required(login_url='staff_login')
def st_schedule_view(request, doctor_id):
    user = CustomUser.objects.get(id= doctor_id)
    doctor = Doctor.objects.get(user= user)
    
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=30)

    available_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=False).order_by("date")
    av_slot_paginator = Paginator(available_slots, 8)
    av_slot_page_num = request.GET.get('page')
    av_slot_page_obj = av_slot_paginator.get_page(av_slot_page_num)

    booked_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=True)
    book_slot_paginator = Paginator(booked_slots, 8)
    book_slot_page_num = request.GET.get('page')
    book_slot_page_obj = book_slot_paginator.get_page(book_slot_page_num)
    context = {
        'doctor': user,
        'available_slots': av_slot_page_obj,
        'booked_slots': book_slot_page_obj,
    }
    return render(request, 'staff/schedule.html', context)


@login_required(login_url='staff_login')
def staff_search(request):
    query = request.GET.get('q', '')
    results = {
        'patients':[],
        'doctors':[],
        'departments':[],
        'appointments':[],
        }

    if query:
        patients = Patient.objects.filter(Q(user__first_name__icontains = query) | Q(user__username__icontains = query))
        doctors = Doctor.objects.filter(Q(user__username__icontains = query) | Q(department__name__icontains = query))
        departments = Department.objects.filter(Q(name__icontains=query))
        appointments = Appointment.objects.filter(
            Q(patient__user__username__icontains = query)|
            Q(doctor__user__username__icontains = query)|
            Q(doctor__department__name__icontains = query)
        ).select_related('doctor', 'patient', 'doctor__department')

        results['patients'] = patients
        results['doctors'] = doctors
        results['departments'] = departments
        results['appointments'] = appointments

        # res_paginator = Paginator(results, 10)
        # res_page_num = request.GET.get('page')
        # res_page_obj = res_paginator.get_page(res_page_num)

    return render(request, 'staff/search_result.html', {'results': results, 'query': query})