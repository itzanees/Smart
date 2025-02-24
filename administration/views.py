from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from . forms import DepartmentCreationForm, UserRegistrationForm, PatientProfileForm, ProfileUpdateForm, PasswordResetRequestForm
from . models import CustomUser, Department, Staff, Doctor, Patient, Schedule, Appointment
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.db.models import Sum
import random, string

# FOR PASSWORD CHANGE
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse


from datetime import datetime, timedelta
from django.utils import timezone
    
def adminLogin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password=password)
        if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_home')
        else:
            messages.error(request, "Invalid credentials or not authorized.")
    return render(request, 'administration/login.html')

def adminForgotPassword(request):
    return render(request, 'administration/forgot-password.html')

@login_required(login_url='admin_login')
@never_cache
def admin_home(request):
    user = request.user
    if user is not None and user.is_superuser:
        doctors = Doctor.objects.all()
        doctor_paginator = Paginator(doctors, 1)
        doctor_page_number = request.GET.get('page')
        doctor_page_obj = doctor_paginator.get_page(doctor_page_number)

        patients = Patient.objects.all()
        patients_paginator = Paginator(patients, 4)
        patients_page_number = request.GET.get('page')
        patients_page_obj = patients_paginator.get_page(patients_page_number)

        appointments = Appointment.objects.filter(appointment_on__date=(timezone.now())).order_by('appointment_on__date')
        appointments_paginator = Paginator(appointments, 1)
        appointments_page_number = request.GET.get('page')
        appointments_page_obj = appointments_paginator.get_page(appointments_page_number)

        notifications = CustomUser.objects.filter(password_request=True)
        
        num_doc = Doctor.objects.all().count()
        num_pat = Patient.objects.all().count()
        num_app = Appointment.objects.all().count()
        revenue = Appointment.objects.aggregate(fees=Sum('doctor__consult_fees'))

        context = {
            'doctors' : doctor_page_obj,
            'num_doc': num_doc,
            'patients' : patients_page_obj,
            'num_pat': num_pat,
            'appointments' : appointments_page_obj,
            'num_app': num_app,
            'revenue': revenue['fees'],
            'notifications':notifications,
        }
        return render(request, 'administration/index.html', context)
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

@login_required(login_url='admin_login')
@never_cache
def admin_profile(request):
    user = request.user
    if user is not None and user.is_superuser:
        today = datetime.today()
        today = str(today)
        form = ProfileUpdateForm(instance=request.user, user=request.user)
        notifications = CustomUser.objects.filter(password_request=True)
        if request.method == "POST":
            form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('admin_profile')
        return render(request, 'administration/profile.html', {'today':today, 'profileform':form,'notifications':notifications,})
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

def intranet(request):
    return render(request, 'intranet.html')

@login_required(login_url='admin_login')
@never_cache
def all_appointment_list(request):
    user = request.user
    if user is not None and user.is_superuser:
        all_appointments = Appointment.objects.all().order_by('-appointment_on__date')
        all_paginator = Paginator(all_appointments, 4)
        all_page_number = request.GET.get('page')
        all_page_obj = all_paginator.get_page(all_page_number)
        notifications = CustomUser.objects.filter(password_request=True)
        return render(request, 'administration/appointment-list.html', {'all_page_obj':all_page_obj,'notifications':notifications,})
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

@login_required(login_url='admin_login')
@never_cache
def appointmentList(request):
    user = request.user
    if user is not None and user.is_superuser:
        latest_appointments = Appointment.objects.filter(appointment_on__date__gte=(timezone.now())).order_by('appointment_on__date')
        latest_paginator = Paginator(latest_appointments, 4)
        latest_page_number = request.GET.get('page')
        latest_page_obj = latest_paginator.get_page(latest_page_number)
        notifications = CustomUser.objects.filter(password_request=True)
        return render(request, 'administration/appointment-list.html', {'latest_page_obj':latest_page_obj,'notifications':notifications,})
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

@login_required(login_url='admin_login')
@never_cache
def specialities(request):
    user = request.user
    if user is not None and user.is_superuser:
        specialities = Department.objects.all()
        specialities_paginator =Paginator(specialities, 8)
        spe_page_num = request.GET.get('page')
        spe_page_obj = specialities_paginator.get_page(spe_page_num)
        notifications = CustomUser.objects.filter(password_request=True)
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
        return render(request, 'administration/departments.html', {'form':form, 'specialities': spe_page_obj,'notifications':notifications,})
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

@login_required(login_url='admin_login')
@never_cache
def users(request):
    user = request.user
    if user is not None and user.is_superuser:
        users = CustomUser.objects.all()
        user_paginator = Paginator(users, 8)
        user_page_num = request.GET.get('page')
        user_page_obj = user_paginator.get_page(user_page_num)
        form = UserRegistrationForm()
        notifications = CustomUser.objects.filter(password_request=True)
        context = {
            'users': user_page_obj,
            'form': form,
            'notifications':notifications,
        }
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active =False
                user.save()

                if user.user_type == 'Doctor':
                    Doctor.objects.create(user = user)
                elif user.user_type == 'Patient':
                    Patient.objects.create(user = user)
                elif user.user_type == 'Staff':
                    Staff.objects.create(user = user)

                current_site = get_current_site(request)
                subject = 'Activate Your Account'
                message = render_to_string('administration/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(subject, message, 'itzanees@gmail.com', [user.email])

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
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.success(request, "Account activated successfully!")
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')
    else:
        return render(request, 'administration/activation_invalid.html')

def forgot_password(request):
    form = PasswordResetRequestForm()
    if request.method =='POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            usr = request.POST.get('username')
            try:
                user = CustomUser.objects.get(username=usr)
                if user:
                    print(user.password_request)
                    user.password_request = True
                    user.save()
                    print(user.password_request)
                    messages.success(request, "Password reset request sent.")
                    return redirect('forgot_password')
            except Exception as e:
                messages.error(request, f"User not found {e}")
                return redirect('forgot_password')
        else:
            messages.error(request, "User not found.")
            return redirect('forgot_password')
    return render(request, 'forgot-password.html', {'form':form})

@login_required(login_url='admin_login')
@never_cache
def users_profile(request, pk):
    user = request.user
    if user is not None and user.is_superuser:
        user = get_object_or_404(get_user_model(), id=pk)
        if request.method == 'POST':
            if 'set_password' in request.POST:
                words = string.ascii_letters
                password = []
                for i in range(10):
                    ran_char = random.choice(words)
                    password.append(ran_char)
                newpassword = ("".join(password))
                user.set_password(newpassword)
                user.password_request = False
                user.save()
                subject = 'Your Temporary Password'
                message = render_to_string('administration/temp_password.html', {
                    'user': user,
                    'newpassword':newpassword,
                    })
                send_mail(subject, message, 'itzanees@gmail.com', [user.email])
                messages.success(request, f"{user.username}'s new password sent to {user.email}")
                return redirect('users_profile', pk) 
            else:
                form = ProfileUpdateForm(request.POST, request.FILES, instance=user, user=user)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"{user.username}'s profile updated")
                    return redirect('users_profile', pk) 
                else:
                    messages.error(request,"Profile is not uptaded!!!")
                    return redirect('users_profile', pk)
        profileform = ProfileUpdateForm(user=user, instance=user)
        return render (request, 'administration/profile.html', {'user':user, 'profileform':profileform})
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

@login_required(login_url='admin_login')
@never_cache
def doctors(request):
    user = request.user
    if user is not None and user.is_superuser:
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
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

@login_required(login_url='admin_login')
@never_cache
def staff(request):
    user = request.user
    if user is not None and user.is_superuser:
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
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

@login_required(login_url='admin_login')
@never_cache
def patients(request):
    user = request.user
    if user is not None and user.is_superuser:
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
    else:
        if request.user.user_type == 'Patient':
            return redirect('patient_dashboard')
        elif request.user.user_type == 'Staff':
            return redirect('staff_dashboard')
        elif request.user.user_type == 'Doctor':
            return redirect('doctor_dashboard')

@login_required(login_url='admin_login')
@never_cache
def Logout(request):
    if request.user.user_type == 'Patient':
        logout(request)
        return redirect(reverse('patient_dashboard'))
    
    elif request.user.user_type == 'Staff':
        logout(request)
        return redirect(reverse('staff_dashboard'))

    elif request.user.user_type == 'Doctor':
        logout(request)
        return redirect(reverse('doctor_dashboard'))
        
    else:
        logout(request)
        return redirect(reverse('admin_home'))
    
def generate_schedule_for_all_doctors():
    today = timezone.now().date()
    date_to = today + timedelta(days=12)

    schedules_to_create = []

    for doctor in Doctor.objects.all():
        current_date = today
        while current_date <= date_to:
            start_time = timezone.datetime.combine(current_date, timezone.datetime.min.time()).replace(hour=9, minute=0)
            end_time = timezone.datetime.combine(current_date, timezone.datetime.min.time()).replace(hour=17, minute=0)

            while start_time < end_time:
                if not Schedule.objects.filter(doctor=doctor, date=current_date, start_time=start_time.time()).exists():
                    schedules_to_create.append(
                        Schedule(
                            doctor=doctor,
                            date=current_date,
                            start_time=start_time.time(),
                            duration=15
                        )
                    )
                start_time += timedelta(minutes=15)

            current_date += timedelta(days=1)

    Schedule.objects.bulk_create(schedules_to_create)

@login_required(login_url='admin_login')
@never_cache
def createschedule(request):
    generate_schedule_for_all_doctors()
    messages.success(request, 'Slots generated')
    return redirect('doctors_list')

@login_required(login_url='admin_login')
@never_cache
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

# @login_required(login_url='admin_login')
# @never_cache
# def book_slot(request, slot_id):
#     slot = Schedule.objects.get(id=slot_id)
#     if request.method == 'POST':
#         patient =Patient.objects.get(user = request.user)
#         print(patient)

#         slot.is_booked = True
#         slot.save()
        
#         Appointment.objects.create(
#             patient =Patient.objects.get(user = request.user),
#             doctor = slot.doctor,
#             appointment_on = slot
#         )

#         return redirect('schedule_view', doctor_id=slot.doctor.user.id)

#     return render(request, 'administration/book-slot.html', {'slot': slot})

@login_required(login_url='admin_login')
@never_cache
class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "change-password.html"
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)

@login_required(login_url='admin_login')
@never_cache
def transaction(request):
    transactions = Appointment.objects.filter(medicalrecord__is_closed=True)
    transactions_paginator = Paginator(transactions, 5)
    transactions_page_num = request.GET.get('page')
    transactions_page_obj = transactions_paginator.get_page(transactions_page_num)
    return render(request, 'administration/transactions-list.html', {'transactions':transactions_page_obj})
