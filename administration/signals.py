from django.db.models.signals import post_save
from django.dispatch import receiver

from . models import CustomUser, Patient, Staff, Doctor

@receiver(post_save, sender =CustomUser)
def create_patient_profile(sender, instance, created, **kwargs):
    if created and instance.user_type =='Patient':
        Patient.objects.create(user = instance)


@receiver(post_save, sender =CustomUser)
def create_staff_profile(sender, instance, created, **kwargs):
    if created and instance.user_type =='Staff':
        Staff.objects.create(user = instance)

@receiver(post_save, sender =CustomUser)
def create_doctor_profile(sender, instance, created, **kwargs):
    if created and instance.user_type =='Doctor':
        Doctor.objects.create(user = instance)