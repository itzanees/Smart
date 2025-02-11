from django import forms
from django.contrib.auth import authenticate
from administration.models import Appointment, Department, Doctor, Schedule, Patient, CustomUser, MedicalRecord
from django.utils import timezone

class DoctorLoginForm(forms.Form):
    username = forms.CharField(
         widget=forms.TextInput(
              attrs= {
                   'class' : 'form-control',
                   'placeholder' : 'Username',
              }
         ),
         label=''
    )
    password = forms.CharField(
         widget=forms.PasswordInput(
         attrs = {
              'class' : 'form-control',
              'placeholder' : 'Password',
         }
        ),
        label=''
    )


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username or password")
        return cleaned_data

class MedicalRecordForm(forms.ModelForm):
     # patient = 
     # doctor
     # appointment
     # department
     # record_date
     notes = forms.Textarea()
     diagnosis = forms.Textarea()
     treatment = forms.Textarea()
     prescription = forms.Textarea()
     attachments = forms.FileInput()

     class Meta:
         model = MedicalRecord
         fields = '__all__'
     #     fields = ['notes', 'diagnosis', 'treatment', 'prescription', 'attachments',]

     
     def __init__(self, *args, **kwargs):
          user = kwargs.pop('user')
          super().__init__(*args, **kwargs)
          
          if hasattr(user, 'patient'):
               self.fields['pat_mrd_no'].initial = user.patient.pat_mrd_no
               
          else:
               self.fields.pop('pat_mrd_no', None)
          if hasattr(user, 'doctor'):
               self.fields['department'].initial = user.doctor.department
          else:
               self.fields.pop('department', None)
          for field_name, field in self.fields.items():
               field.widget.attrs['class'] = 'form-control'
               field.widget.attrs['placeholder'] = field.label
               field.help_text = None
               
               if field_name == 'date' or field_name == 'end_date':
                    field.widget = forms.DateInput(attrs={
                         'type': 'text',
                         'class': 'form-control',
                         'disabled': True,
                         'min' : str(timezone.now().date()),
                         'max' : str(timezone.now().date()),
                         })

