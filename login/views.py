from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .forms import LoginForm, ResetForm, EmailForm, Security, OTPForm
from django.http import HttpResponse
from registration.models import Registration
from django.core.mail import send_mail
from random import randrange
from django.core.mail import send_mail
import base64

# User login
def loginreq(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        log_username = request.POST['username']
        log_password = request.POST['password']
        log_user = authenticate(username=log_username,password=log_password)
        if log_user is not None:
            login(request, log_user)
            request.session['username']=log_username
            user = User.objects.get(username=log_username)
            curr_user = Registration.objects.get(reg_user=user)
            context = {'log_username':log_username,'log_password':log_password,'log_firstname':user.first_name,
            'log_lastname':user.last_name,'log_email':user.email,'log_mobile':curr_user.reg_MobileNumber,'log_custid':curr_user.reg_CustomerId,
            'log_sec':curr_user.reg_SecurityQuestion,'log_ans':curr_user.reg_SecurityAnswer}
            return render(request,'index.html',{'context':context})    
        else:
            return render(request,'login.html',{'form':form, 'message':'Invalid Credentials'})
    else:
        form = LoginForm()
        return render(request,'login.html',{'form':form})

# User logout
def auth_logout(request):
    if request.session.get('username'):
       del request.session['username']
    logout(request)
    return HttpResponse("<h1>Logged out Successfully</h1>")

#Reset Password
def log_password(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            password1 = request.POST['password1'] 
            pass_email = request.session['email']    
            pass_user = User.objects.get(email=pass_email)
            pass_user.set_password(password1)
            pass_user.save() #save new password in database
            message = 'Password changed successfully'
            if 'email' in request.session:
                del request.session['email']
            if 'verify_otp' in request.session:
                del request.session['verify_otp']
            form = LoginForm()
            return render(request,'login.html',{ 'form': form,'message' : message})
        else:
            context = 'Invalid Password'
            return render(request,'password_reset.html',{'form':form, 'context' : context})
    else:
        form = ResetForm()
        return render(request,'password_reset.html',{'form' : form})

# Receiving email from user for Password reset
def pass_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        pass_email = request.POST['email']
        request.session['email'] = pass_email
        if pass_email:
            try:
                pass_user = get_object_or_404(User,email = pass_email)
            except:
                return render(request,'password_mail.html',{'form' : form, 'message':'Email not registered'})
            else:
               
                return render(request,'password_choice.html')
        else:
            return render(request,'password_mail.html',{'form' : form, 'message':'Email field is required'})
    else:
        form = EmailForm()
        return render(request,'password_mail.html',{'form' : form})

#Generating OTP 
def generateOTP():
    otp = randrange(100000,999999)
    return str(otp)

#Sending OTP to user's registered email
def pass_otp(request):
    pass_email = request.session['email']
    pass_otp = generateOTP()
    #sending email
    send_mail('OTP Validation','Your OTP is '+str(pass_otp),'easygo.docs@gmail.com',[pass_email],fail_silently=False)
    request.session['verify_otp'] = pass_otp
    return redirect('verify_otp')

#Verifying OTP
def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        pass_entered_otp = request.POST['OTP']
        if pass_entered_otp:
            pass_verify_otp = request.session['verify_otp'] 
            if pass_entered_otp == pass_verify_otp:  #OTP validation
                return redirect('reset') #Redirect to password reset page
            else:
                message = 'Invalid OTP'
                return render(request,'otp_form.html',{ 'form':form, 'message': message})
        else:
            message = 'OTP is required'
            return render(request,'otp_form.html',{'message': message})
    else:
        form = OTPForm()
        return render(request, 'otp_form.html',{'form':form})

#Verifying Security Answer
def pass_sec(request):
    pass_email = request.session['email']
    pass_user = User.objects.get(email = pass_email)
    pass_curr_user = Registration.objects.get(reg_user=pass_user)
    context =  pass_curr_user.reg_SecurityQuestion
    if request.method == 'POST':
        form = Security(request.POST)
        pass_sec_ans = request.POST['security_answer']
        if pass_sec_ans:
            if pass_sec_ans == pass_curr_user.reg_SecurityAnswer:  #Security Answer Validation
                return redirect('reset')  #Redirect to password reset page
            else:
                message = 'Invalid Answer'
                return render(request,'password_sec.html',{'form':form,'message': message, 'context':context})
        else:
            message = "Security Answer is required"
            return render(request, 'password_sec.html',{'form':form, 'context':context, 'message':message})
    else:
            form = Security()
            return render(request, 'password_sec.html',{'form':form,'context':context })
                


    






         





    




