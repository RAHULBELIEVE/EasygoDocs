from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import RegexValidator



# Create your models here.
Country_Code = (
    ('+91','+91(India)'),
    ('+1', '+1(USA)'),
)
QTN_CHOICES = (("What is your first pet's name?", "What is your first pet's name?"),
    ('Who is your favorite teacher?', 'Who is your favorite teacher?'),
    ('What is the name of the town where you were born?', 'What is the name of the town where you were born?'),
    ( 'What elementary school did you attend?', 'What elementary school did you attend?'))
GEN_CHOICES =(('male',"Male"),('female',"Female"),('others',"Others"))

class Registration(models.Model):
    reg_user = models.OneToOneField(User, on_delete=models.CASCADE)
    #additional fields
    reg_SecurityQuestion = models.CharField(max_length=100,choices=QTN_CHOICES, default="What is your first pet's name?")
    reg_SecurityAnswer = models.CharField(max_length=100)
    reg_ReferalId = models.CharField(default = 'default',max_length=50)
    reg_CustomerId = models.CharField(default = 'default', max_length=50)
    reg_Gender = models.CharField(max_length=10,choices=GEN_CHOICES, default='male')
    reg_MainBalance = models.IntegerField(default=75)
    reg_RewardsPoints = models.IntegerField(default=25)
    reg_is_cancelled = models.BooleanField(default=False)
    reg_is_revoked = models.BooleanField(default=False)
    reg_profile_pic = models.ImageField(default='./static/registration/images/default.jpg')
    reg_CountryCode = models.CharField(max_length=5,choices=Country_Code, default='+91')
    phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Phone number must be entered in the format: '9999999999'. Up to 15 digits allowed.")
    reg_MobileNumber = models.CharField(validators=[phone_regex], max_length=15) # validators should be a list
    
    def __str__(self):
         return self.reg_user.username +" "+str(self.reg_MainBalance)


# class Document(models.Model):
#     description = models.CharField(max_length=255, blank=True)
#     document = models.FileField(upload_to='documents/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)