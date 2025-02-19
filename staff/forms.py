from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from administration.models import CustomUser

class CustomLoginForm(forms.Form):
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
    


class InPatientRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
            model = CustomUser
            fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'gender', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].label = 'Contact Number'
        self.fields['password2'].label = 'Confirm Password'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = None