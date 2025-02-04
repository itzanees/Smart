from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from . forms import DepartmentCreationForm, UserRegistrationForm, PatientProfileForm, ProfileUpdateForm, SheduleCreatorForm
from . models import CustomUser, Department, Staff, Doctor, Patient, Schedule, Appointment
from django.contrib import messages
from django.core.paginator import Paginator

from datetime import datetime, timedelta
from django.utils import timezone

# @permission_required(appname.viewname)
def adminLogin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        admin = authenticate(request, username =username, password=password)
        if admin is not None and admin.is_superuser:
                login(request, admin)
                return redirect('admin_home')
        else:
            messages.error(request, "Invalid credentials or not authorized as admin.")
    return render(request, 'administration/login.html')

def adminForgotPassword(request):
    return render(request, 'administration/forgot-password.html')

@login_required(login_url='admin_login')
def adminHome(request):
    return render(request, 'administration/index.html')

def adminProfile(request):
    today = datetime.today()
    today = str(today)
    form = ProfileUpdateForm(instance=request.user, user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')
    return render(request, 'administration/profile.html', {'today':today, 'profileform':form})

def intranet(request):
    return render(request, 'intranet.html')

def all_appointment_list(request):
    all_appointments = Appointment.objects.all()
    all_paginator = Paginator(all_appointments, 4)
    all_page_number = request.GET.get('page')
    all_page_obj = all_paginator.get_page(all_page_number)
    return render(request, 'administration/appointment-list.html', {'all_page_obj':all_page_obj})

def appointmentList(request):
    latest_appointments = Appointment.objects.filter(appointment_on__date__gte=(timezone.now()))
    latest_paginator = Paginator(latest_appointments, 4)
    latest_page_number = request.GET.get('page')
    latest_page_obj = latest_paginator.get_page(latest_page_number)

    return render(request, 'administration/appointment-list.html', {'latest_page_obj':latest_page_obj})

def specialities(request):
    specialities = Department.objects.all()
    specialities_paginator =Paginator(specialities, 8)
    spe_page_num = request.GET.get('page')
    spe_page_obj = specialities_paginator.get_page(spe_page_num)
    form = DepartmentCreationForm()
    if request.method == 'POST':
        if 'delete_department' in request.POST:
            dep_id = request.POST.get('dep_id')
            dep = get_object_or_404(Department, id=dep_id)
            dep.delete()
            messages.success(request, f"Deleted {dep.name}")
            return redirect('specialities')

        if 'edit_department' in request.POST:
            dep_id = request.POST.get('dep_id')
            dep = get_object_or_404(Department, id = dep_id)
            form = DepartmentCreationForm(request.POST, request.FILES, instance = dep)
            if form.is_valid():
                form.save()
                messages.success(request, "Modifid Successfully")
                return redirect('specialities')
            else:
                messages.error(request, "Error Occured")
                return redirect('specialities')

        else:
            form = DepartmentCreationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Created new department successfully")
                return redirect('specialities')
            else:
                messages.error(request, "Unable to create specialities")
                return redirect('specialities')

    form = DepartmentCreationForm()
    return render(request, 'administration/specialities.html', {'form':form, 'specialities': spe_page_obj})

def users(request):
    users = CustomUser.objects.all()
    user_paginator = Paginator(users, 8)
    user_page_num = request.GET.get('page')
    user_page_obj = user_paginator.get_page(user_page_num)
    form = UserRegistrationForm()
    context = {
        'users': user_page_obj,
        'form': form,
    }
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_type == 'Doctor':
                Doctor.objects.create(user = user)
            elif user.user_type == 'Patient':
                Patient.objects.create(user = user)
            elif user.user_type == 'Staff':
                Staff.objects.create(user = user)
            messages.success(request, f"User {user.username} Created")
            return redirect('users')
        
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(CustomUser, id=user_id)
            user.delete()
            messages.success(request, f"Deleted User {user.username}")
            return redirect('users')
        
        elif form.is_valid() == False:
            for error in form.errors:
                messages.error(request, form.errors[error])
                return redirect('users')
        else:
            return render(request, 'administration/users.html', context)    
    return render(request, 'administration/users.html', context)

def usersProfile(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user, user=user)
        if form.is_valid():
            form.save()
            return redirect('users_profile', pk) 
    profileform = ProfileUpdateForm(user=user, instance=user)
    return render (request, 'administration/profile.html', {'user':user, 'profileform':profileform})

@login_required
def doctors(request):
    doctors = CustomUser.objects.filter(user_type='Doctor').order_by('created_at')
    doc_paginator = Paginator(doctors, 8)
    doc_page_num = request.GET.get('page')
    doc_page_obj = doc_paginator.get_page(doc_page_num)
    if request.method == "POST":
            user_id = request.POST.get('doc_id')
            user = get_object_or_404(CustomUser, id=user_id)
            user.delete()
            messages.success(request, f"Deleted {user.username}")
            return redirect('doctors_list')
    context = {
        'doctors':doc_page_obj,
    }
    return render(request, 'administration/doctor-list.html', context)

@login_required
def staff(request):
    staffs = CustomUser.objects.filter(user_type='Staff')
    staff_paginator = Paginator(staffs, 8)
    staff_page_num = request.GET.get('page')
    staff_page_obj = staff_paginator.get_page(staff_page_num)
    if request.method == "POST":
            staff_id = request.POST.get('staff_id')
            staff = get_object_or_404(CustomUser, id=staff_id)
            staff.delete()
            messages.success(request, f"Staff {staff.username} deleted")
            return redirect('staff_list')
    context = {
        'staffs' : staff_page_obj,
    }
    return render(request, 'administration/staff-list.html', context)

@login_required
def patients(request):
    patients = CustomUser.objects.filter(user_type='Patient')
    pat_paginator = Paginator(patients, 8)
    pat_page_num = request.GET.get('page')
    pat_page_obj = pat_paginator.get_page(pat_page_num)
    if request.method == "POST":
            pat_id = request.POST.get('pat_id')
            pat = get_object_or_404(CustomUser, id=pat_id)
            pat.delete()
            messages.success(request, f"Patient {pat.username} deleted")
            return redirect('patients_list')
    patient_profile_form = PatientProfileForm()
    context = {
            'patients':pat_page_obj,
              'pat_prof':patient_profile_form,
            }    
    return render(request, 'administration/patient-list.html', context)



@login_required
def Logout(request):
    if request.user.user_type == 'Patient':
        logout(request)
        return redirect('patient_dashboard') 
    elif request.user.user_type == 'Staff':
        logout(request)
        return redirect('staff_dashboard')
    elif request.user.user_type == 'Doctor':
        logout(request)
        return redirect('doctor_dashboard')
    else:
        logout(request)
        return redirect('admin_home')

def generate_schedule_for_doctor():
    today = datetime.today()
    six_months_later = today + timedelta(days=30)

    for doctor in Doctor.objects.all():
        current_date = today
        while current_date <= six_months_later:
            start_time = datetime.combine(current_date, datetime.min.time()).replace(hour=9) 
            end_time = datetime.combine(current_date, datetime.min.time()).replace(hour=17)  

            while start_time < end_time:
                if not Schedule.objects.filter(doctor=doctor, date=current_date, start_time=start_time.time()).exists():
                    Schedule.objects.create(
                        doctor=doctor,
                        date=current_date,
                        start_time=start_time.time(),
                        duration=30 
                    )
                start_time += timedelta(minutes=30)

            current_date += timedelta(days=1)

@login_required
def createschedule(request):
    generate_schedule_for_doctor()
    messages.success(request, 'Slots generated')
    return redirect('doctors_list')
 





# MANUAL SCHEDULE CREATION
# def createschedule(request, doctor_id):
#     form = SheduleCreatorForm()
#     doctor = CustomUser.objects.get(id= doctor_id)
#     doctor_profile = Doctor.objects.get(user= doctor)

#     if request.method == "POST":
#         form = SheduleCreatorForm(request.POST)
#         if 'create_schedule' in request.POST:
#             date = request.POST.get('date')
#             end_date = request.POST.get('end_date')
#             start_time = request.POST.get('start_time')
#             end_time = request.POST.get('end_time')
#             duration = request.POST.get('duration')

#             start_time_obj = datetime.strptime(start_time, "%H:%M").time()
#             end_time_obj = datetime.strptime(end_time, "%H:%M").time()

#             if not Schedule.objects.filter(
#                                             doctor=doctor_profile,
#                                             date__range=[date, end_date],
#                                             start_time__lte=end_time_obj,
#                                             end_time__gte=start_time_obj
#                                             ).exists():
#                 generate_schedule_for_doctor(doctor_profile, date, end_date, start_time, end_time, duration)
#             else:
#                 print("Same data Exists")
#                 error = 'Schedule date or time already exists..!!!'
#                 return render(request, 'administration/createschedule.html', {'form':form, 'error':error })
#             return redirect('schedule_view', doctor_id)
#     return render(request, 'administration/createschedule.html', {'form':form})
    
# @login_required
def schedule_view(request, doctor_id):
    user = CustomUser.objects.get(id= doctor_id)
    doctor = Doctor.objects.get(user= user)
    
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=30)

    available_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=False).order_by("date")
    av_slot_paginator = Paginator(available_slots, 8)
    av_slot_page_num = request.GET.get('page')
    av_slot_page_obj = av_slot_paginator.get_page(av_slot_page_num)

    booked_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=True)
    book_slot_paginator = Paginator(booked_slots, 8)
    book_slot_page_num = request.GET.get('page')
    book_slot_page_obj = book_slot_paginator.get_page(book_slot_page_num)
    context = {
        'doctor': user,
        'available_slots': av_slot_page_obj,
        'booked_slots': book_slot_page_obj,
    }
    return render(request, 'administration/schedule.html', context)

@login_required
def book_slot(request, slot_id):
    slot = Schedule.objects.get(id=slot_id)
    if request.method == 'POST':
        patient =Patient.objects.get(user = request.user)
        print(patient)

        slot.is_booked = True
        slot.save()
        
        Appointment.objects.create(
            patient =Patient.objects.get(user = request.user),
            doctor = slot.doctor,
            appointment_on = slot
        )

        return redirect('schedule_view', doctor_id=slot.doctor.user.id)

    return render(request, 'administration/book-slot.html', {'slot': slot})

# FOR PASSWORD CHANGE
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "change-password.html"
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)

# @login_required(login_url='patient_login')
# def change_password(request):
#     if request.method == "POST":
#         form = CustomPasswordChangeForm(user = request.user, data = request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user) 
#             messages.success(request, "Password Changed Successfully")
#             return redirect("password_change_done")
#     else:
#         form = CustomPasswordChangeForm(user=request.user)
#     return render(request, 'change-password.html', {'form':form})


def transaction(request):
    return render(request, 'administration/transactions-list.html')
