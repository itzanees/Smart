from django import forms
from django.contrib.auth import authenticate
from administration.models import CustomUser, MedicalRecord, Doctor
from django.forms.widgets import DateInput

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

class DoctorPasswordResetRequestForm(forms.Form):
    username = forms.CharField(
         widget=forms.TextInput(
              attrs= {
                   'class' : 'form-control',
                   'placeholder' : 'Username',
              }
         ),
         label=''
    )

    def clean(self):
     cleaned_data = super().clean()
     username = cleaned_data.get("username")
     user = CustomUser.objects.get(username=username)
     try:
         doctor = Doctor.objects.get(user=user)
         return cleaned_data
     except Exception as e:
         raise forms.ValidationError("Invalid username.")

class MedicalRecordForm(forms.ModelForm):
    next_appointment = forms.DateTimeField(
    required=False,
    widget=DateInput(attrs={
        'class': 'form-control',
        'type': 'date',
        'placeholder': 'Select next appointment date'
    })
    )
    class Meta:
        model = MedicalRecord
        fields = ['notes', 'diagnosis', 'treatment', 'prescription', 'attachments']
        
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter notes'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter diagnosis'}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter treatment'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter prescription'}),
        }

    def __init__(self, *args, **kwargs):
        super(MedicalRecordForm, self).__init__(*args, **kwargs)
        self.fields['attachments'].widget.attrs.update({'class': 'form-control'})