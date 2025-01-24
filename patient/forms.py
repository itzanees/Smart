from django import forms
from django.contrib.auth import authenticate


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