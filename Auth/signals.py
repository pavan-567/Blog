from .models import User 
from Profile.models import Profile, ProfileVerification
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .emails import send_account_activation_email

@receiver(post_save, sender= User)
def send_email_token(sender, instance, created, **kwargs) : 
    try : 
        if created : 
            email_token = str(uuid.uuid4())
            
            # Handling Profile Stuff
            profile = Profile.objects.create(user= instance)
            profile_verf = ProfileVerification.objects.create(profile= profile, email_token= email_token)
            profile.save()
            profile_verf.save()

            # Getting Email
            email = instance.email 
            send_account_activation_email(email, email_token)
    except Exception as e :
        print(e)