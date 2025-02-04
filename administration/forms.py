from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, Department, Doctor, Patient, Schedule
from datetime import datetime, date, timedelta
from django.utils import timezone

class PatientRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].label = 'Contact Number'
        self.fields['password2'].label = 'Confirm Password'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = None
            if field_name == 'date_of_birth':
                field.widget = forms.DateInput(attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Date of Birth',
                    'max' : str(date.today()),
                    'onclick':"(this.type='date')",
                    'onblur':"(this.type='text')",
                })

class DepartmentCreationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'dep_image', 'description', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = None
            if field_name == 'description':
                field.widget = forms.TextInput(
                    attrs={
                        'type' : 'textarea',
                        'rows' : '2',
                        'class' :'form-control',
                        'placeholder': field.label, 
                    }
                )
            if field_name == 'is_active':    
                field.widget = forms.CheckboxInput(
                    attrs={
                        'class' : 'form-control',
                    }
                )
                field.label = ('Is Active?')

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
            model = CustomUser
            fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'gender', 'email', 'phone_number', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].label = 'Contact Number'
        self.fields['password2'].label = 'Confirm Password'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = None

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user']


class ProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    ]
    # Fields from CustomUser
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=10,required=True)
    profile_pic = forms.ImageField(required=False)
    date_of_birth = forms.DateField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    address1 = forms.CharField(max_length=128,required=True)
    address2 = forms.CharField(max_length=123,required=False)
    city = forms.CharField(max_length=32,required=True)
    state = forms.CharField(max_length=32,required=True)
    pincode = forms.CharField(max_length=6,required=True)
    country = forms.CharField(max_length=32,required=True)
    

    # Fields from Patient
    pat_mrd_no = forms.CharField(disabled=True)

    # Fields from Doctors
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, empty_label="Select Department",)
    employ_code = forms.CharField(disabled=True)
    qualification = forms.CharField(max_length=64, required=True)
    license_number = forms.CharField(max_length=32, required=True)
    consult_fees = forms.DecimalField(max_digits=6, decimal_places=2)
    
    # Fields from StaffProfile
    role = forms.CharField(max_length=20, required=False)
    employee_code = forms.CharField(disabled=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name','last_name', 'date_of_birth', 'gender', 'email', 'phone_number', 'profile_pic', 'address1', 'address2', 'city', 'state', 'pincode', 'country']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        if hasattr(user, 'patient'):
            self.fields['pat_mrd_no'].initial = user.patient.pat_mrd_no
        else:
            self.fields.pop('pat_mrd_no', None)


        if hasattr(user, 'doctor'):
            self.fields['department'].initial = user.doctor.department
            self.fields['employ_code'].initial = user.doctor.employ_code
            self.fields['qualification'].initial = user.doctor.qualification
            self.fields['license_number'].initial = user.doctor.license_number
            self.fields['consult_fees'].initial = user.doctor.consult_fees
        else:
            self.fields.pop('department', None)
            self.fields.pop('employ_code', None)
            self.fields.pop('qualification', None)
            self.fields.pop('license_number', None)
            self.fields.pop('consult_fees', None)

        if hasattr(user, 'staff'):
            self.fields['role'].initial = user.staff.role
            self.fields['employee_code'].initial = user.staff.employee_code
        else:
            self.fields.pop('role', None)
            self.fields.pop('employee_code', None)


        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = None
            if field_name == 'date_of_birth':
                field.widget = forms.DateInput(attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Date of Birth',
                    'max' : str(date.today()),
                    'onclick':"(this.type='date')",
                    'onblur':"(this.type='text')",
                })

    def save(self, commit=True):
        user = super().save(commit=commit)

        # Save UserProfile fields
        if hasattr(user, 'patient'):
            profile = user.patient
            profile.pat_mrd_no = self.cleaned_data['pat_mrd_no']
            if commit:
                profile.save()

        # Save StaffProfile fields
        if hasattr(user, 'staff'):
            staff_profile = user.staff
            staff_profile.role = self.cleaned_data['role']
            staff_profile.employee_code = self.cleaned_data['employee_code']
            if commit:
                staff_profile.save()

        if hasattr(user, 'doctor'):
            doctor_profile = user.doctor
            doctor_profile.department = self.cleaned_data['department']
            doctor_profile.employ_code = self.cleaned_data['employ_code']
            doctor_profile.qualification = self.cleaned_data['qualification']
            doctor_profile.license_number = self.cleaned_data['license_number']
            doctor_profile.consult_fees = self.cleaned_data['consult_fees']
            if commit:
                doctor_profile.save()

        return user
    
# def generate_schedule_for_doctor(doctor, date, end_date, start_time, end_time, duration):
#         start_date = date
#         end_date = end_date
        
#         current_date = start_date
#         while current_date <= end_date:
#             start_time = datetime(start_date.year, start_date.month, start_date.day, start_time.time, start_time.minute)
#             end_time = datetime(end_date.year, end_date.month, end_date.day, end_time.time, end_time.minute)
            
#             while start_time < end_time:
#                 Schedule.objects.create(
#                     doctor=doctor,
#                     date=current_date,
#                     end_date=end_date,
#                     start_time=start_time.time(),
#                     end_time=end_time.time(),
#                     duration=duration,
#                 )
#                 start_time += timedelta(minutes=duration)  # Move to the next slot
#             current_date += timedelta(days=1)

class SheduleCreatorForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['doctor','date', 'end_date','start_time', 'end_time','duration']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = None

            if field_name == 'date' or field_name == 'end_date':
                field.widget = forms.DateInput(attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'mm/dd/yyyy',
                    'min' : str(timezone.now().date() + timedelta(days = 3)),
                    'max' : str(timezone.now().date() + timedelta(days=33)),
                    'onclick':"(this.type='date')",
                    'onblur':"(this.type='text')",
                })

            
            if field_name == 'start_time' or field_name == 'end_time':
                field.widget = forms.TimeInput(attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Time Slot',
                    'min' : str(timezone.now().time()),
                    'onclick':"(this.type='time')",
                    'onblur':"(this.type='text')",
                })


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder' : "Enter Current Passaword",
            }),
        label='Current Password'
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder' : "Enter New Password",
            }),
        label='New Password'
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder' : "Confirm New Password",
            }),
        label='Confirm New Password'
    )
