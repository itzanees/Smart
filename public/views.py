from django.shortcuts import render, redirect
from administration.models import ContactUs
from django.contrib import messages

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
    if request.method == "POST":
        name  = request.POST['name']
        email = request.POST['email']
        phone_num = request.POST['phone_num']
        contact_type = request.POST['contact_type']
        message  = request.POST['message']

        try:
            c = ContactUs (
                name = name,
                email = email,
                phone_num = phone_num,
                contact_type = contact_type,
                message = message
            )
            c.save()
            messages.success(request, "Message Submitted")
            return redirect('contact')
        
        except Exception as e:
            messages.error(request, f"Message not submitted, {e}")
            return redirect('contact')
        
    return render(request, 'public/contact.html')

def webAppointment(request):
    today = datetime.date.today()
    today = str(today)
    return render(request, 'public/search-appointment.html', {'today':today})

def tos(request):
    return render(request, 'public/tos.html')

def privacy(request):
    return render(request, 'public/privacy.html')