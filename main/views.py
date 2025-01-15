from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def departments(request):
    return render(request, 'main/departments.html')

def doctors(request):
    return render(request, 'main/doctors.html')

def services(request):
    return render(request, 'main/services.html')

def contact(request):
    return render(request, 'main/contact.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def webAppointment(request):
    return render(request, 'main/book-appointment.html')