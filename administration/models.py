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
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
         return self.username

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dep_image = models.ImageField(upload_to='department/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=32,default='')

    def __str__(self):
         return self.name

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    pat_mrd_no = models.CharField(max_length=32,unique=True)
    
    def save(self, *args, **kwargs):
        if not self.pat_mrd_no:
            last_profile = Patient.objects.last()
            last_id = int(last_profile.pat_mrd_no.split('-')[1]) if last_profile else 12500001
            self.pat_mrd_no = f"SPT-{last_id + 1}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# class Schedule(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='schedule')
#     date = models.DateField()
#     time_slot = models.TimeField(unique=True)
#     is_available = models.BooleanField(default=True)


class   Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    employ_code = models.CharField(max_length=32, unique=True)
    qualification = models.CharField(max_length=64)
    license_number  = models.CharField(max_length=32, unique=True, null=True, blank=True)
    consult_fees = models.DecimalField(max_digits=6, decimal_places=2, default=100, null=True, blank=True)
    slug = models.SlugField(max_length=32,default='')
    # experience_years = models.IntegerField()
    def save(self, *args, **kwargs):
        if not self.employ_code:
            last_profile = Doctor.objects.last()
            last_id = int(last_profile.employ_code.split('-')[1]) if last_profile else 250001
            self.employ_code = f"SDC-{last_id + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedule')
    date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True,blank=True)
    duration = models.PositiveIntegerField(help_text='Slot Duration in Minutes')
    is_booked = models.BooleanField(default=False)
    slug = models.SlugField(max_length=32, default='')

    class Meta:
        unique_together = ['doctor', 'date', 'start_time']
    
    
    def __str__(self):
        return f'Schedule of {self.doctor} - {self.date} {self.start_time}'

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
        ('CO', 'Completed')
    ]

    appointment_number = models.CharField(max_length=32, unique=True)    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_on = models.OneToOneField(Schedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule')
    appointment_fees = models.DecimalField(max_digits=6,decimal_places=2, default='100')
    status = models.CharField(max_length=2, choices=STATUS, default='SH')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=32 ,default='')
    
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
    TYPES = [
         ('CN', 'Consultaion Note'),
         ('LR', 'Lab Report'),
         ('PR', 'Prescription')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=2, choices=TYPES)
    record_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField()
    attachments = models.FileField(upload_to='mrd/', null=True, blank=True)


class Billing(models.Model):
    PSTATUS= [
       ('PD','Paid'),
       ('PE', 'Pending'),
       ('UP', 'Unpaid')
    ]

    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    bill_no = models.CharField(max_length=32)
    date = models.DateTimeField()
    consult_charge = models.DecimalField(max_digits=6,decimal_places=2)
    medication_charge = models.DecimalField(max_digits=10,decimal_places=2)
    procedure_charge = models.DecimalField(max_digits=10,decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=PSTATUS)

    def save(self, *args, **kwargs):
        if not self.bill_no:
            last_inv = Billing.objects.last()
            today = f"{datetime.today().year}{datetime.today().month}{datetime.today().day}"
            last_id = int(last_inv.appointment_number.split('-')[1]) if last_inv else 1
            self.appointment_number = f"SINV-{today}000{last_id + 1}"
        super().save(*args, **kwargs)