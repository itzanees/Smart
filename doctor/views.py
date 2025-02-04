from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.utils import timezone
import calendar
from administration.models import Schedule

def doctorLogin(request):
    return render(request, 'doctor/login.html')

def doctorForgotPassword(request):
    return render(request, 'doctor/forgot-password.html')

# @login_required
def doctorHome(request):
    return render(request, 'doctor/index.html')

def doctorProfile(request):
    today = timezone.now()
    today = str(today)
    return render(request, 'doctor/profile.html', {'today':today})

def schedules(request):
    today = timezone.now()
    year = today.year
    month = today.month
    todate = today.day
    days_in_month = calendar.monthrange(year, month)[month]
    days = [datetime(year, month, day) for day in range(todate, days_in_month + 1)]

    if request.method == 'POST':
        time_slot = request.POST.get('time_slot')
        selected_day = request.POST.get('selected_day') 
        print(selected_day)
       
        if selected_day and time_slot:
            event_date = datetime.strptime(selected_day, '%Y-%m-%d')
            event_date = event_date.date()
            print(event_date)
            event = Schedule(date=event_date, time_slot=time_slot)
            event.save()
            return redirect('calendar_view')  

    schedules = Schedule.objects.all()
    context = {
        'days': days,
        'schedules':schedules,
    }
    # return render(request, 'calen.html', context)
    # days = calendar.month(1)
    text_cal = calendar.TextCalendar()
    formatted_month = text_cal.formatmonth(2025, 1)
    # print(days)
    return render(request, 'doctor/schedule.html', {'days':formatted_month})

def drAppointmentList(request):
    return render(request, 'doctor/appointment-list.html')


def patients(request):
    return render(request, 'doctor/patient-list.html')