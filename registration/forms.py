from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator


class RegistrationForm(UserCreationForm):
    # giving choices 
    QTN_CHOICES = [('','Security Question'),("What is your first pet's name?", "What is your first pet's name?"),
    ('Who is your favorite teacher?', 'Who is your favorite teacher?'),
    ('What is the name of the town where you were born?', 'What is the name of the town where you were born?'),
    ( 'What elementary school did you attend?', 'What elementary school did you attend?')]
    
    GEN_CHOICES =[('',"Gender"),('male',"Male"),('female',"Female"),('others',"Others")]

    COUNTRY_CODE = [('','Country Code'),('+91','+91(India)'),
    ('+1', '+1(USA)')]
    # phone number with regex validations
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Phone number must be entered in the format: '9999999999'. Up to 15 digits allowed.")
    reg_MobileNumber = forms.CharField(label='Mobile Number',validators=[phone_regex], max_length=15,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone number'})) # validators should be a list
    reg_CountryCode = forms.CharField(max_length=5,label='Country Code', widget=forms.Select(choices=COUNTRY_CODE,attrs={'class': 'form-control'}))
    reg_SecurityAnswer = forms.CharField(label='Security Answer',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Security Answer'}))
    reg_ReferalId = forms.CharField(label='Referal Id',max_length=50, required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Referral ID'}))
    reg_Terms = forms.BooleanField(label='Terms & Conditions')
    reg_Gender = forms.CharField(max_length=10,label='Gender', widget=forms.Select(choices=GEN_CHOICES,attrs={'class': 'form-control'}))
    reg_SecurityQuestion= forms.CharField(max_length=100,label='Security Question', widget=forms.Select(choices=QTN_CHOICES,attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','email','reg_CountryCode','reg_MobileNumber','reg_Gender',
                'username','reg_SecurityQuestion','reg_SecurityAnswer','password1','password2','reg_ReferalId'
                ]
        widgets ={
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':"Firstname"}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control','placeholder':"Lastname"}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':"Email"}),
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder':"Username"}),
            # 'password1': forms.PasswordInput(attrs={'class':'forsm-control','placeholder':"Password"}),
            # 'password2': forms.PasswordInput(attrs={'class':'form-control','placeholder':"Confirm Password"})
            }

            # 'name': forms.TextInput(attrs={'class':'form-control'}),
            # 'email': forms.EmailInput(attrs={'class':'form-control'}),
            # 'password' :forms.PasswordInput(attrs={'class':'form-control'})
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email must be unique')
        return email
    