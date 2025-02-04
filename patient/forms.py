from django import forms
from django.contrib.auth import authenticate
from administration.models import Appointment, Department, Doctor, Schedule, Patient, CustomUser
from django.contrib.auth.forms import PasswordChangeForm

from datetime import date, timedelta
from django.utils import timezone

class PatientLoginForm(forms.Form):
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
    

class BookAppointmentForm(forms.ModelForm):
     department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department")
     doctor = forms.ModelChoiceField(queryset=Doctor.objects.none(), label="Doctor", required=False)
     schedule = forms.ModelChoiceField(queryset=Schedule.objects.none(), label="Available Schedules", required=False)
    
     class Meta:
        model = Appointment
        fields = ['department','doctor','appointment_on','status']

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
          for field_name, field in self.fields.items():
               field.widget.attrs['class'] = 'form-control'
               field.widget.attrs['placeholder'] = field.label
               field.help_text = None
               # if field_name == 'department':
               #      field.widget = forms.Select(attrs={
               #           'title' :'Department', 
               #           'placeholder': 'department',
               #      })


class UserProfileUpdateForm(forms.ModelForm):
    # Fields from CustomUser
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=10,required=True)
    profile_pic = forms.ImageField(required=False)
    date_of_birth = forms.DateField()
    address1 = forms.CharField(max_length=128,required=True)
    address2 = forms.CharField(max_length=123,required=False)
    city = forms.CharField(max_length=32,required=True)
    state = forms.CharField(max_length=32,required=True)
    pincode = forms.CharField(max_length=6,required=True)
    country = forms.CharField(max_length=32,required=True)
    

    # Fields from Patient
    pat_mrd_no = forms.CharField(disabled=True)


    class Meta:
        model = CustomUser
        fields = [ 'profile_pic', 'username', 'first_name','last_name', 'date_of_birth', 'email', 'phone_number', 'address1', 'address2', 'city', 'state', 'pincode', 'country']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        if hasattr(user, 'patient'):
            self.fields['pat_mrd_no'].initial = user.patient.pat_mrd_no
        else:
            self.fields.pop('pat_mrd_no', None)

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

#     def save(self, commit=True):
#         user = super().save(commit=commit)
#         return user

class DocSearchForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput, required=False)
    gender = forms.MultipleChoiceField(choices=[('M', 'Male Doctor'), ('F','Female Doctor')], required=False,
                                       widget=forms.CheckboxSelectMultiple,
                                       )
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False,
                                                widget = forms.Select(attrs={
                                                    'class' : 'form-control'
                                                }))

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.help_text = None
            if field_name == 'date':
                field.widget = forms.DateInput(attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Date',
                    'min' : timezone.now().date() + timedelta(days = 2),
                    'onclick':"(this.type='date')",
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
