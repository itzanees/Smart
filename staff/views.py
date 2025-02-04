from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
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

import datetime

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
    appointments = Appointment.objects.filter(appointment_on__date__gte = (datetime.date.today()))[:4]
    context = {
        'appointments':appointments,
        'doctors':doctors,
        'patients':patients,
    }
    return render(request, 'staff/index.html', context)

def appointmentList(request):
    appointments = Appointment.objects.filter(appointment_on__date__gte = (datetime.date.today()))
    return render(request, 'staff/appointment-list.html', {'appointments':appointments})

def staff_transaction(request):
    appointments = Appointment.objects.filter(appointment_on__date__gte = (datetime.date.today()))
    return render(request, 'staff/transactions-list.html', {'appointments': appointments})

def staff_specialities(request):
    specialities = Department.objects.all()
    return render(request, 'staff/specialities.html', {'specialities':specialities})

def staff_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'staff/doctor-list.html', {'doctors':doctors})

def staff_patients(request):
    patients = Patient.objects.all()
    if request.method=='POST':
        pat_id = request.POST.get('pat_id')
        pat_id = int(pat_id)
        pat_user = CustomUser.objects.get(id = pat_id)
        modal_class = 'show'
        form = ProfileUpdateForm(instance=pat_user, user=pat_user)
        return render(request, 'staff/patient-list.html', {'patients':patients, 'profileform':form, 'modal':modal_class, 'pat_id':pat_id})
    return render(request, 'staff/patient-list.html', {'patients':patients})