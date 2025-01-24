from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from administration.models import CustomUser, Patient
from administration.forms import PatientRegistrationForm
from .forms import PatientLoginForm
from django.contrib import messages
import datetime

# def adminLogin(request):
#     return render(request, 'admin/login.html')

def patForgotPassword(request):
    return render(request, 'patient/forgot-password.html')

@login_required(login_url='patient_login')
def patientHome(request):
    return render(request, 'patient/index.html')


def patientLogin(request):
    if request.method == 'POST':
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username= username, password=password)
            if user is not None and user.user_type == 'Patient':
                login(request, user)
                return redirect('patient_dashboard')
            
    else:
        form = PatientLoginForm()
    return render(request, 'patient/login.html', {'form':form})

def patientRegistration(request):
    form = PatientRegistrationForm()
    if request.method =='POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user_type = 'Patient'
            patient.save()
            return redirect('patient_login')
        else:
            return render(request, 'patient/register.html', {'form' : form})
    return render(request, 'patient/register.html', {'form':form})

@login_required
def patientProfile(request):
    today = datetime.date.today()
    today = str(today)
    try:
        profile = Patient.objects.get(user=request.user)
        for p in profile:
            print(p)
    except Exception as e:
        print("No Profiles - ")
    
    return render(request, 'patient/profile.html', {'today':today})

def appointment(request):
    return render(request, 'patient/appointment.html')

# def bookings(request):
    # return render(request, 'admin/bookings.html')

def transaction(request):
    return render(request, 'patient/transactions-list.html')

def specialities(request):
    return render(request, 'patient/specialities.html')

def doctors(request):
    return render(request, 'patient/doctor-list.html')

def services(request):
    return render(request, 'patient/services.html')

