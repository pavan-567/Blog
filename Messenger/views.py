from django.shortcuts import render, redirect
from Auth.models import User 
from .models import Room, UserMessages
from django.template.defaultfilters import slugify
from datetime import datetime, timezone
from Profile.models import Profile
from django.contrib.auth.decorators import login_required

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# Create your views here.


# Helper Function Which Converts UTC To IST
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


@login_required
def MessageRoom(request, pk) :
    # Get The User
    user = request.user

    # Get Other User Who is to be interested
    other_user = User.objects.get(id= pk)
    last_seen = utc_to_local(other_user.profile.updated_at) 

    difference = (datetime.now().date() - last_seen.date()).days
    print(f'Diff for {request.user.username} : {difference}')


    # Get Unique Dates
    dates = []
    messages = []
    for userMsg in UserMessages.objects.values('pure_date').order_by('pure_date').distinct() : 
        print(userMsg['pure_date'])
        messages.append( { userMsg['pure_date'] : UserMessages.objects.filter(pure_date= userMsg['pure_date']) })
    
    # Logic
    status = None 
    if(difference == 0) : 
        status = "Today"
    elif difference == 1 : 
        status = "Yesterday"
    elif difference <= 6 : 
        status = days[last_seen.weekday()]
    else : 
        status = last_seen.strftime("%b") + " " + str(last_seen.weekday()) # % B = Full Month, %b = ShortForm Of Month

    # Generating Slug and Room
    usernames = user.username + other_user.username 
    revusernames = other_user.username + user.username

    room = None
    roomName = None

    # Checking If Room Exists or not
    if Room.objects.filter(slug= slugify(usernames)).exists() or Room.objects.filter(slug= slugify(revusernames)).exists() : 
        print("IN EXISTING ROOM!")
        # If Room Already Present, Retrieve The Information
        if Room.objects.filter(slug= slugify(usernames)).exists() :
            room = Room.objects.get(slug= slugify(usernames))
            roomName = slugify(usernames)
        else : 
            room = Room.objects.get(slug= slugify(revusernames))
            roomName = slugify(revusernames)

        # Check and add User to the room
        if not Room.objects.filter(users= user).exists() : 
            room.users.add(user)
            room.save()
    else : 
        # Creating a Room
        print("NEW ROOM!")
        room = Room.objects.create(name= usernames, slug= slugify(usernames))
        roomName = slugify(usernames)
        
        # Adding User to the room
        room.users.add(user)

        # Saving Room
        room.save()

    context = {
        'room': room,
        'UserMessages': messages,
        'receiver': other_user,
        'status' : status,
        'messageDates': dates
    }

    return render(request, 'Messenger/communicate.html', context)


@login_required
def ChangeChatWallpaper(request, receiver_pk) : 
    user = request.user 
    profile = Profile.objects.get(user= user)

    if request.method == "POST" : 
        print(request.FILES)
        img = request.FILES.get('chat-image')
        profile.chat_wallpaper = img 
        profile.save()

    return redirect('message', pk= receiver_pk)

@login_required
def SetDefaultChatWallpaper(request, receiver_pk) : 
    user = request.user 
    profile = Profile.objects.get(user= user)
    profile.set_image_to_default()
    return redirect('message', pk= receiver_pk)