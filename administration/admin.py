from django.contrib import admin

from .models import CustomUser, Staff, Patient, Doctor

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'employee_code', 'hire_date', 'is_active')
    search_fields = ('user__username', 'role')
    list_filter = ('role', 'is_active')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'employ_code')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender')
    search_fields = ('user__username')

admin.site.register(Patient)
