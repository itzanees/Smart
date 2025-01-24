from django.shortcuts import render
from django.http import HttpResponse
from localflavor.in_.in_states import STATE_CHOICES

import datetime

def home(request):
    return render(request, 'public/index.html')

def about(request):
    return render(request, 'public/about.html')

def departments(request):
    return render(request, 'public/departments.html')

def doctors(request):
    return render(request, 'public/doctors.html')

def services(request):
    return render(request, 'public/services.html')

def contact(request):
    return render(request, 'public/contact.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def webAppointment(request):
    today = datetime.date.today()
    today = str(today)
    return render(request, 'public/search-appointment.html', {'today':today})

def intranet(request):
    return render(request, 'staff/intranet.html')

def tos(request):
    return render(request, 'public/tos.html')

def privacy(request):
    return render(request, 'public/privacy.html')