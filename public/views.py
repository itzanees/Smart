from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

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
    return render(request, 'public/book-appointment.html')