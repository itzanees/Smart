from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from administration.models import CustomUser, Patient, Department, Doctor, Schedule, Appointment
from administration.forms import PatientRegistrationForm
from .forms import PatientLoginForm, UserProfileUpdateForm, DocSearchForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
# FOR PASSWORD CHANGE
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def patient_registration(request):
    form = PatientRegistrationForm()
    if request.method =='POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user_type = 'Patient'
            patient.save()
            Patient.objects.create(user = patient)
            messages.success(request, "Account created, Now you can Login to patient portal")
            return redirect('patient_login')
        else:
            return render(request, 'patient/register.html', {'form' : form})
    return render(request, 'patient/register.html', {'form':form})

def patient_login(request):
    if request.method == 'POST':
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username= username, password=password)
            if user is not None and user.user_type == 'Patient' or user.is_superuser:
                login(request, user)
                return redirect('patient_dashboard')
            else:
                messages.error(request, 'Unauthorized!!!')
                return redirect('patient_login')
    else:
        form = PatientLoginForm()
    return render(request, 'patient/login.html', {'form':form})

def pat_forgot_password(request):
    return render(request, 'patient/forgot-password.html')



@login_required(login_url='patient_login')
def pat_change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("password_change_done")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change-password.html', {'form':form})


@login_required(login_url='patient_login')
def patient_dashboard(request):
    if request.user.user_type != 'patient':
        patient = Patient.objects.get(user=request.user)
        if patient.profile_updated:
            return render(request, 'patient/patient-dashboard.html')
        else:
            return redirect('patient_profile')
    else:
        user = CustomUser.objects.get(id = request.user.id)
        patient = Patient.objects.get(user = request.user)      # getting user from request
        appointments = Appointment.objects.filter(patient = patient).order_by('appointment_on')
        return render(request, 'patient/patient-dashboard.html', {'user':user, 'appointments':appointments})

@login_required(login_url='patient_login')
def patient_profile(request):
    try:
        user = get_object_or_404(get_user_model(), id=request.user.id)
        if request.method == 'POST':
            form = UserProfileUpdateForm(request.POST, request.FILES, instance=user, user=user)
            try:
                if form.is_valid():
                    form.save()
                    patient, created = Patient.objects.get_or_create(user=user)
                    patient.pat_mrd_no = form.cleaned_data['pat_mrd_no']
                    patient.blood_group = form.cleaned_data['blood_group']
                    patient.profile_updated = True
                    patient.save()
                    messages.success(request, f"{user.username}'s profile updated")
                    return redirect('patient_profile') 
                else:
                    messages.error(request, f"{user.username}'s please check information and try again")
                    return redirect('patient_profile') 
            except Exception as e:
                print(e)
        profileform = UserProfileUpdateForm(user=user, instance=user)
        today = datetime.today
        today = str(today)
    # try:
    #     profile = Patient.objects.get(user=request.user)
    #     for p in profile:
    #         print(p)
    except Exception as e:
        print("No Profiles - ", e)
    
    return render(request, 'patient/profile-settings.html', {'today':today, 'profileform':profileform })

# def appointment(request):
    
#     # doctor = Doctor.objects.get(id = )
#     departments=Department.objects.all()
#     # form = BookAppointmentForm()
#     context = {
#         'departments':departments,
#         # 'form':form,
#     }
#     return render(request, 'patient/booking.html', context)

def appointment_dep(request, pk):
    path = request.path
    dep_id = int(path.split('/')[3])
    doctors = Doctor.objects.filter(department_id = dep_id)
    return render(request, 'patient/appointment.html', {'doctors':doctors})

def appointment_doc(request, pk):
    path = request.path
    doc_id = int(path.split('/')[4])
    doctor = Doctor.objects.get(id = pk)
    today = timezone.now()
    # bookable_day = today+timedelta(days=3)
    bookable_day = today
    schedules = Schedule.objects.filter(doctor_id = doc_id, is_booked = False, date__gte = bookable_day  ).order_by('date')
    context = {
        'schedules':schedules,
        'doctor':doctor,
    }
    return render(request, 'patient/booking.html', context)

def appointment_sch(request, pk):
    path = request.path
    schedule_id = int(path.split('/')[4])
    today = start_date = timezone.now().date()
    end_date = start_date + timedelta(days=10)
    schedules = Schedule.objects.filter(doctor_id = schedule_id, is_booked =False)
    dates = {}
    
    current_date = today
    while current_date <= end_date:
        # dates[current_date.strftime('%b. %d, %Y')] =  current_date.strftime('%b. %d, %Y')# Format date as string (optional)
        dates[current_date] =  current_date 

        current_date += timedelta(days=1)  # Increment by one day

    for i  in dates:
        print(type(dates[i]))
                
    print(schedules)
    return render(request, 'patient/booking.html', {'dates':dates, 'schedules':schedules})
    # return render(request, 'patient/appointment.html', {'dates':dates, 'schedules':schedules})


def bookings(request):
    return render(request, 'patient/booking.html')

def hosp_specialities(request):
    specialities = Department.objects.all()
    return render(request, 'patient/specialities.html',{'specialities':specialities})

def doc_hosp_specialities(request, pk):
    department = Department.objects.get(id = pk)
    doctors = Doctor.objects.filter(department = department)
    return render (request, 'patient/specialities.html',{'doctors':doctors})


def hos_doctors_list(request):
    doctors = CustomUser.objects.filter(user_type='Doctor')
    context = {
        'doctors':doctors,
    }

    return render(request, 'patient/doctor-list.html', context)

def pat_doctor_profile(request, pk):
    doctor = Doctor.objects.get(id=pk)
    context = {
        'doctor':doctor,
    }

    return render(request, 'patient/doctor-profile.html', context)

def pat_schedule_view(request, doctor_id):
    user = CustomUser.objects.get(id= doctor_id)
    doctor = Doctor.objects.get(user= user)

    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=30)

    available_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=False)
    booked_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=True)

    context = {
        'doctor': user,
        'available_slots': available_slots,
        'booked_slots': booked_slots,
    }
    return render('patient/schedule.html', context)

def hosp_services(request):
    return render(request, 'patient/services.html')

def doc_search(request):
    doctors = Doctor.objects.all()
    form = DocSearchForm()

    if request.method =="POST":
        form = DocSearchForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            gender = form.cleaned_data.get('gender')
            department = form.cleaned_data.get('department')
            results = Q()

            if gender:
                results &= Q(user__gender__in=gender)
            if department:
                results &= Q(department=department)
            if date:
                results &= Q(schedule__date =date, schedule__is_booked=False)
                
            doctors = doctors.filter(results).distinct()

            context ={
                'form':form,
                'doctors':doctors,
                # 'departments' : departments,
                    }
            return render (request, 'patient/search.html', context)

    context ={
        'doctors':doctors,
        'form':form,
    }

    return render (request, 'patient/search.html', context)

@login_required(login_url='patient_login')
def pat_search(request):
    query = request.GET.get('q', '')
    results = {
        'doctors':[],
        'departments':[],
        }

    if query:
        doctors = Doctor.objects.filter(Q(user__username__icontains = query) | Q(department__name__icontains = query))
        departments = Department.objects.filter(Q(name__icontains=query))

        results['doctors'] = doctors
        results['departments'] = departments


    return render(request, 'patient/search_result.html', {'results': results, 'query': query})



@login_required(login_url='patient_login')
def pat_schedule_view(request, doctor_id):
    user = CustomUser.objects.get(id= doctor_id)
    doctor = Doctor.objects.get(user= user)
    
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=30)

    available_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=False)
    booked_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=True)

    context = {
        'doctor': user,
        'available_slots': available_slots,
        'booked_slots': booked_slots,
    }
    return render(request, 'administration/schedule.html', context)

@login_required(login_url='patient_login')
def pat_book_slot(request, slot_id):
    slot = Schedule.objects.get(id=slot_id)
    if request.method == 'POST':
        patient =Patient.objects.get(user = request.user)
        doctor =Doctor.objects.get(user = slot.doctor.user.id)
        date = slot.date
        # check if patient already have appointment with same doctor same date
        bookings = Appointment.objects.filter(doctor = doctor, patient = patient)
        is_found = False
        for i in bookings:
            if i.appointment_on.date == date:
                is_found =True
                break

        if is_found:
            error = "You already have a booking on this date."
            return render(request, 'patient/book-slot.html', {'slot': slot, 'error':error})
        else:
            slot.is_booked = True
            slot.save()
            Appointment.objects.create(
                patient =Patient.objects.get(user = request.user),
                doctor = slot.doctor,
                appointment_on = slot
            )
            messages.success(request, "Appointment booked Successfully!")
            return redirect('pat_book_success')
    return render(request, 'patient/book-slot.html', {'slot': slot})

def pat_book_success(request):
    appointment = Appointment.objects.all().order_by('created_at').last()
    print(appointment)
    return render(request, 'patient/booking-success.html', {'appointment':appointment})


def view_pat_bill(request):
    return render(request, 'patient/invoice-view.html')