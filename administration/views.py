from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from . forms import DepartmentCreationForm, UserRegistrationForm, PatientProfileForm, ProfileUpdateForm, SheduleCreatorForm
from . models import CustomUser, Department, Staff, Doctor, Patient, Schedule
from django.contrib import messages

from datetime import datetime, timedelta
from django.utils import timezone

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

def appointmentList(request):
    return render(request, 'administration/appointment-list.html')

def transaction(request):
    return render(request, 'administration/transactions-list.html')

def specialities(request):
    specialities = Department.objects.all()
    form = DepartmentCreationForm()
    if request.method == 'POST':
        if 'delete_department' in request.POST:
            dep_id = request.POST.get('dep_id')
            dep = get_object_or_404(Department, id=dep_id)
            dep.delete()
            return redirect('specialities')
        
        if 'edit_department' in request.POST:
            dep_id = request.POST.get('dep_id')
            dep = get_object_or_404(Department, id = dep_id)
            form = DepartmentCreationForm(request.POST, request.FILES, instance = dep)
            if form.is_valid():
                form.save()
                return redirect('specialities')
        else:
            form = DepartmentCreationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('specialities')
    

    form = DepartmentCreationForm()
    return render(request, 'administration/specialities.html', {'form':form, 'specialities': specialities})

def users(request):
    users = CustomUser.objects.all()
    form = UserRegistrationForm()
    context = {
        'users': users,
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
            return redirect('users')
        
        if 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(CustomUser, id=user_id)
            user.delete()
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

def doctors(request):
    doctors = CustomUser.objects.filter(user_type='Doctor')
    if request.method == "POST":
            user_id = request.POST.get('doc_id')
            user = get_object_or_404(CustomUser, id=user_id)
            user.delete()
            return redirect('doctors_list')
    context = {
        'doctors':doctors,
    }
    return render(request, 'administration/doctor-list.html', context)

def staff(request):
    staffs = CustomUser.objects.filter(user_type='Staff')
    if request.method == "POST":
            staff_id = request.POST.get('staff_id')
            staff = get_object_or_404(CustomUser, id=staff_id)
            staff.delete()
            return redirect('staff_list')
    context = {
        'staffs' : staffs,
    }
    return render(request, 'administration/staff-list.html', context)

def patients(request):
    patients = CustomUser.objects.filter(user_type='Patient')
    if request.method == "POST":
            pat_id = request.POST.get('pat_id')
            pat = get_object_or_404(CustomUser, id=pat_id)
            pat.delete()
            return redirect('patients_list')
    patient_profile_form = PatientProfileForm()
    return render(request, 'administration/patient-list.html', {'patients':patients, 'pat_prof':patient_profile_form})



@login_required
def Logout(request):
    if request.user.user_type == 'Patient':
        logout(request)
        return redirect('patient_dashboard') 
    elif request.user.user_type == 'Administrator':
        logout(request)
        return redirect('admin_home')



def generate_schedule_for_doctor(doctor, duration=30):
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=2)  # 6 months from now
    
    current_date = start_date
    while current_date <= end_date:
        # Generate time slots for each day
        start_time = datetime(current_date.year, current_date.month, current_date.day, 9, 0)  # Starting at 9 AM
        end_time = datetime(current_date.year, current_date.month, current_date.day, 10, 0)  # Ending at 5 PM
        
        while start_time < end_time:
            # Create the time slot for this doctor
            Schedule.objects.create(
                doctor=doctor,
                date=current_date,
                start_time=start_time.time(),
                duration=duration
            )
            start_time += timedelta(minutes=duration)  # Move to the next slot
        current_date += timedelta(days=1)

# @login_required
def schedule_view(request, doctor_id):
    form = SheduleCreatorForm()
    user = CustomUser.objects.get(id= doctor_id)
    doctor = Doctor.objects.get(user= user)
    
    if request.method == "POST":
        form = SheduleCreatorForm(request.POST)
        if 'create_schedule' in request.POST:
            doc_id = request.POST.get('doc_id')
            form.save()
            return redirect('schedule_view', doc_id)
    
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=180)

    available_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=False)
    booked_slots = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date], is_booked=True)

    context = {
        'form':form,
        'doctor': user,
        'available_slots': available_slots,
        'booked_slots': booked_slots,
    }
    return render(request, 'administration/schedule.html', context)

@login_required
def book_slot(request, slot_id):
    slot = Schedule.objects.get(id=slot_id)
    if request.method == 'POST':
        slot.is_booked = True
        slot.save()
        return redirect('schedule_view', doctor_id=slot.doctor.user.id)

    return render(request, 'administration/book-slot.html', {'slot': slot})

