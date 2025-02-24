from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.utils import timezone

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    ]

    USER_TYPE_CHOICES = [
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Staff', 'Staff'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='', null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    country = models.CharField(max_length=32, default='', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    password_request = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.username
    
    def save(self, *args, **kwargs):
        if self.is_superuser and self._state.adding:
            # This is a superuser being created
            self.is_active = True
        super().save(*args, **kwargs)

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dep_image = models.ImageField(upload_to='department/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
         return self.name

class Patient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+','A+'),
        ('A-','A-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('B+','B+'),
        ('B-','B-'),
        ('O+','O+'),
        ('O-','O-'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    pat_mrd_no = models.CharField(max_length=32,unique=True)
    profile_updated = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pat_mrd_no:
            last_profile = Patient.objects.last()
            last_id = int(last_profile.pat_mrd_no.split('-')[1]) if last_profile else 12500000
            self.pat_mrd_no = f"SPT-{last_id + 1}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient- {self.user.first_name} {self.user.last_name}."

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    employ_code = models.CharField(max_length=32, unique=True)
    qualification = models.CharField(max_length=64)
    license_number  = models.CharField(max_length=32, unique=True, null=True, blank=True)
    consult_fees = models.DecimalField(max_digits=6, decimal_places=2, default=100, null=True, blank=True)
    profile_updated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.employ_code:
            last_profile = Doctor.objects.last()
            last_id = int(last_profile.employ_code.split('-')[1]) if last_profile else 250000
            self.employ_code = f"SDC-{last_id + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}\' Profile"

class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedule')
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(help_text='Slot Duration in Minutes')
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ['doctor', 'date', 'start_time']
        get_latest_by = ['created_at']

    def __str__(self):
        return f'Schedule of {self.doctor} - {self.date} {self.start_time}'


def generate_schedule_for_doctor():
    today = datetime.today()
    date_to = today + timedelta(days=10)
    for doctor in Doctor.objects.all():
        current_date = today
        while current_date <= date_to:
            start_time = datetime.combine(current_date, datetime.min.time()).replace(hour=9) 
            end_time = datetime.combine(current_date, datetime.min.time()).replace(hour=13)  

            while start_time < end_time:
                if not Schedule.objects.filter(doctor=doctor, date=current_date).exists():
                    Schedule.objects.create(
                        doctor=doctor,
                        date=current_date,
                        start_time=start_time.time(),
                        duration=15
                    )
                    print(doctor)
                start_time += timedelta(minutes=15)

            current_date += timedelta(days=1)
            
class Staff(models.Model):
    ROLE_CHOICES = [
        ('Receptionist', 'Receptionist'),
        ('Nurse', 'Nurse'),
        ('Pharmacist', 'Pharmacist'),
    ]

    user = models.OneToOneField('administration.CustomUser', on_delete=models.CASCADE, related_name='staff')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    employee_code = models.CharField(max_length=32, unique=True)
    hire_date = models.DateField(auto_now_add=True)
    profile_updated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.employee_code:
            last_profile = Staff.objects.last()
            last_id = int(last_profile.employee_code.split('-')[1]) if last_profile else 20250000
            self.employee_code = f"STF-{last_id + 1}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"

class Appointment(models.Model):
    STATUS = [
        ('SH', 'Scheduled'),
        ('RP', 'Reported'),
        ('CO', 'Completed'),
        ('CA', 'Cancelled'),
        ('NS', 'Noshow'),
    ]

    appointment_number = models.CharField(max_length=32, unique=True)    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_on = models.OneToOneField(Schedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule')
    # appointment_fees = models.DecimalField(max_digits=10,decimal_places=2, default='100')
    status = models.CharField(max_length=2, choices=STATUS, default='SH')
    follow_up = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.appointment_number:
            last_appt = Appointment.objects.last()
            today = f"{datetime.today().year}{datetime.today().month}{datetime.today().day}"
            last_id = int(last_appt.appointment_number.split('-')[2]) if last_appt else 0
            self.appointment_number = f"SAPT-{today}-{last_id + 1}"

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.patient.user.username}'s booking with {self.doctor}"
    
class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True)
    notes = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    attachments = models.FileField(upload_to='mrd/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_opened = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.patient.user.username}'s Medical Record."

class ContactUs(models.Model):
    CONACT_TYPES = [
        ('ME', "Message"),
        ('EQ', 'Enquiry'),
        ('SU', 'Suggestion'),
        ('CO', 'Complaint'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_num = models.CharField(max_length=10)
    contact_type = models.CharField(max_length=2, choices=CONACT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

# class Billing(models.Model):
#     PSTATUS= [
#        ('PD','Paid'),
#        ('PE', 'Pending'),
#        ('UP', 'Unpaid')
#     ]

#     staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     bill_no = models.CharField(max_length=32)
#     date = models.DateTimeField()
#     consult_charge = models.DecimalField(max_digits=6,decimal_places=2)
#     medication_charge = models.DecimalField(max_digits=10,decimal_places=2)
#     procedure_charge = models.DecimalField(max_digits=10,decimal_places=2)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=2, choices=PSTATUS, default='PE')

#     def save(self, *args, **kwargs):
#         if not self.bill_no:
#             last_inv = Billing.objects.last()
#             today = f"{datetime.today().year}{datetime.today().month}{datetime.today().day}"
#             last_id = int(last_inv.appointment_number.split('-')[1]) if last_inv else 1
#             self.appointment_number = f"SINV-{today}000{last_id + 1}"
#         super().save(*args, **kwargs)