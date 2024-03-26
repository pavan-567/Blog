from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from .forms import UserForm
from .models import User
from Profile.models import Profile, ProfileVerification
from django.contrib import messages
from uuid import uuid4
from .emails import send_forget_password_email, send_account_activation_email

# Create your views here.

def Login(request) : 
    if request.user.is_authenticated : 
        return redirect("home")
    
    if request.method == "POST" : 
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email= email, password= password)


        if user is not None : 
            login(request, user)
            return redirect('home')
        else : 
            messages.error(request, 'Either of email or password is Incorrect!')
        
    return render(request, "Auth/login.html")


def Logout(request) :
    user = request.user 
    user.profile.status = False 
    logout(request)
    return redirect('login')

def Register(request) : 
    if request.user.is_authenticated : 
        return redirect('home')
    
    form = UserForm() 

    if request.method == "POST" : 
        form = UserForm(request.POST)

        if form.is_valid() : 
            form.save()
            messages.success(request, "An email has been sent to your mail!")
            return redirect(request.path_info)
        else : 
            messages.error(request, "Enter all the details correctly!")
            
    context = {'form': form}
    return render(request, "Auth/register.html", context)

def Verify_Email(request) : 
    user = request.user 
    email = user.email 
    profile_verf = user.profile.profileverification
    email_token = str(uuid4())
    profile_verf.email_token = email_token
    profile_verf.save()

    send_account_activation_email(email, email_token)

    messages.success(request, 'An Email Has Been Sent! Kindly Check In Your Inbox')
    return redirect('login')

    


def Activate_Email(request, email_token) : 
    try : 
        prof = ProfileVerification.objects.get(email_token= email_token)
        prof.is_email_verified = True
        prof.save()

        # Authentication
        print(prof)

        login(request, prof.profile.user)
        messages.success('Your Email Has Been Successfully Verified!')
        return redirect('edit-profile')
    except Exception as e : 
        return HttpResponse("Invalid Email!")
    
# User When Enters mail and submits
def Forgot_Password(request) : 
    if request.method == "POST" :  
        email = request.POST.get('email')
        if not User.objects.filter(email= email).exists() : 
            messages.warning(request, "Invalid Email!")
            return redirect('login')
        
        user = User.objects.get(email= email)
        profile = Profile.objects.get(user= user)
        prof_ver = profile.profileverification

        token = str(uuid.uuid4())
        prof_ver.forgot_password_token = token
        prof_ver.save()

        send_forget_password_email(email= email, token= token)
        messages.success(request, "An Email Is Sent!")
    
    return redirect('login')

# New Page For Password
def Change_Password(request, password_token) : 
    context = {}
    try : 
        profileVer = ProfileVerification.objects.filter(forgot_password_token= password_token).first()
        profile = profileVer.profile
        
        if request.method == "POST" : 
            new_password = request.POST['new_pass']
            confirm_password = request.POST['confirm_pass']
            user_id = request.POST.get('user_id')

            if user_id is None : 
                messages.error(request, 'INVALID USER! [Wrong USER ID!]')
                return redirect(request.path_info)
            
            if new_password != confirm_password : 
                messages.error(request, "Password's aren't matched!")
                return redirect(request.path_info)
            
            user = User.objects.get(id= user_id)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully!')
        

            return redirect('login')
        
        context = {'user_id': profile.user.id}
    except Exception as e : 
        print(e)
    return render(request, 'Auth/change-password.html', context)
