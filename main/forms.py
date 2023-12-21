# forms.py

from django import forms
from .models import Feedback

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email')
 
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=4, widget=forms.TextInput(attrs={'type': 'number', 'inputmode': 'numeric'}))


class ContactForm(forms.ModelForm):
    class Meta:
        print("3")
        model = Feedback
        fields = ['first_name', 'last_name', 'email', 'mobile', 'message']
