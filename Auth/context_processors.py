from .models import User 

def allUsers(request) : 
    return {'activeUsers': User.objects.filter(profile__status= True), 'inactiveUsers': User.objects.filter(profile__status= False)}