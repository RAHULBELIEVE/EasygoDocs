from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    

    class Meta():
        model = User
        fields = ['username','password']

class ResetForm(UserCreationForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    #password1 = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ['password1','password2']

class EmailForm(UserCreationForm):
    #email = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['email']

class OTPForm(forms.Form):
    OTP = forms.CharField(max_length=6)
    class Meta:
        fields = ['OTP']
class Security(forms.Form):
    security_answer = forms.CharField(max_length=100)
    class Meta:
        #model = Registration
        fields = ['security_answer']





