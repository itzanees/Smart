from django.shortcuts import render
from django.http import HttpResponse

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

def webAppointment(request):
    today = datetime.date.today()
    today = str(today)
    return render(request, 'public/search-appointment.html', {'today':today})

def tos(request):
    return render(request, 'public/tos.html')

def privacy(request):
    return render(request, 'public/privacy.html')