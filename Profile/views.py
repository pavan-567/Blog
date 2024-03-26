from django.shortcuts import redirect, render
from .forms import ProfileForm
from Auth.forms import UserUpdationForm
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
def Profile_Follow_Unfollow(request, pk) : 
    profile = Profile.objects.get(id= pk)
    if request.method == "POST" : 
        current_user_profile = request.user.profile

        action = request.POST.get('follow')

        if action == 'follow' : 
            current_user_profile.follows.add(profile)
        else : 
            current_user_profile.follows.remove(profile)

        current_user_profile.save()
    print(f"Profile : {profile}")
    return render(request, 'Profile/main.html', {"profile": profile})



@login_required
def Edit(request) : 
    if request.method == "POST" : 

        print(request.POST)
        user_form = UserUpdationForm(request.POST or None, instance= request.user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None,instance= request.user.profile)

        if user_form.is_valid() and profile_form.is_valid() : 
            user_form.save() 
            profile_form.save() 
            return redirect('profile', pk= request.user.profile.id)


    user_form = UserUpdationForm(instance= request.user)
    profile_form = ProfileForm(instance= request.user.profile)

    context = {
        'u_form': user_form,
        'p_form': profile_form
    }

    return render(request, 'Profile/edit.html', context)

