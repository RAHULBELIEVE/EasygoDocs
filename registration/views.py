from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import Registration
from django.http import HttpResponse
from datetime import date
from django.core.mail import send_mail
# Create your views here.


def first3(prev_Customer_id): #Generating Customer id 
    k = prev_Customer_id[0:3]
    a1=k[0];a2=k[1];a3=k[2];r=a1+a2+a3
    if r!="ZZZ":
        a3=chr(ord(a3)+1)
        if ord(a3)>90:
            a2=chr(ord(a2)+1)
            a3="A"
            if ord(a2)>90:
                a1=chr(ord(a1)+1)
                a2="A"
        r=a1+a2+a3
    return r

def CreateAccount(request): #Registering User
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            reg_Firstname = request.POST['first_name']
            reg_Lastname = request.POST['last_name']
            reg_Email = request.POST['email']
            reg_CountryCode = request.POST['reg_CountryCode']
            reg_MobileNumber = request.POST['reg_MobileNumber']
            reg_UserName = request.POST['username']
            reg_password1 = request.POST['password1']
            reg_password2 = request.POST['password2']
            reg_SecurityQuestion = request.POST['reg_SecurityQuestion']
            reg_SecurityAnswer = request.POST['reg_SecurityAnswer']
            reg_ReferalId = request.POST['reg_ReferalId'] 
            reg_Gender = request.POST['reg_Gender']
            reg_CustomerId = ''
                        
            reg_user = User.objects.create_user(username=reg_UserName,first_name=reg_Firstname,last_name=reg_Lastname,email=reg_Email,password=reg_password1)
            id_Count = Registration.objects.count() # total records count in table
            if id_Count == 0:
                reg_CustomerId = 'AAA0000'
            else:
                last_record = Registration.objects.last() # Get Last Record .
                prev_CustomerId = last_record.reg_CustomerId
                k=prev_CustomerId[0:3];last_digit=prev_CustomerId[3:7];last_digit=int(last_digit);last_digit=last_digit+1
                if last_digit>9999:
                    reg_CustomerId=first3(k)+"{:04d}".format(0)
                else:
                    reg_CustomerId=k+"{:04d}".format(last_digit)
                          
            newuser = Registration(reg_user=reg_user,reg_CountryCode=reg_CountryCode,reg_MobileNumber=reg_MobileNumber,reg_SecurityQuestion=reg_SecurityQuestion,reg_SecurityAnswer=reg_SecurityAnswer,reg_ReferalId=reg_ReferalId, reg_Gender=reg_Gender,reg_CustomerId=reg_CustomerId)
            newuser.save() # saveing records
            if len(reg_ReferalId) != 0:
                try:
                    reg_available = get_object_or_404(Registration,reg_CustomerId=reg_ReferalId)
                except:
                    messages = {'warning_message':'Invalid Referral Id'}
                    return render(request,'signup.html',{'form':form,'messages':messages})
                else:
                    reg_available.reg_RewardsPoints = reg_available.reg_RewardsPoints+10
                    reg_available.save()

            # sending mail ...
            send_mail('Welcome to Iotrix','You have sucessfully registered. Your customer id is '+reg_CustomerId,'easygo.docs@gmail.com',[reg_Email],fail_silently=False,)
            # returning successfull page .
            return HttpResponse("<h1>Your credentials saved Successfully, you can login our main page</h1>")
                       
           
    else:
        form = RegistrationForm() # method not created , so else part will execute
    return render(request,'signup.html',{'form':form})

