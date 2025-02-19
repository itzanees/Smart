from django import forms
from administration.models import ContactUs

class ContactUsForm(forms.Form):
    CONACT_TYPES = [
        ('ME', "Message"),
        ('EQ', 'Enquiry'),
        ('SU', 'Suggestion'),
        ('CO', 'Complaint'),
    ]

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone_num = forms.CharField(max_length=10, required=True)
    contact_type = forms.ChoiceField(choices=CONACT_TYPES)
    message = forms.Textarea()

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone_num', 'contact_type', 'message']

    