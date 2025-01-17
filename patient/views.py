from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required,permission_required

import datetime

# def adminLogin(request):
#     return render(request, 'admin/login.html')

# def adminForgotPassword(request):
#     return render(request, 'admin/forgot-password.html')

# @login_required
def patientHome(request):
    return render(request, 'patient/index.html')

# def adminProfile(request):
#     today = datetime.date.today()
#     today = str(today)
#     return render(request, 'admin/profile.html', {'today':today})

# def appointmentList(request):
#     return render(request, 'admin/appointment-list.html')

# def transaction(request):
#     return render(request, 'admin/transactions-list.html')

# def specialities(request):
#     return render(request, 'admin/specialities.html')

# def doctors(request):
#     return render(request, 'admin/doctor-list.html')

# def patients(request):
#     return render(request, 'admin/patient-list.html')