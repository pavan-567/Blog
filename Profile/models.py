from django.db import models
from Auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, null= True)
    bio = models.TextField()
    image = models.ImageField(default= 'def_cute.png', upload_to= 'profile', validators= [
        FileExtensionValidator(['png', 'jpg', 'jpeg'])
    ])
    cover = models.ImageField(default= 'cover.png', upload_to= 'cover', null= True, validators= [FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    chat_wallpaper = models.ImageField(default= 'chat_def.jpg', upload_to= 'chat', null= True, validators= [FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    follows = models.ManyToManyField("self", related_name= "followed_by", symmetrical= False, blank= True)
    status = models.BooleanField(default= False)    
    updated_at = models.DateTimeField(auto_now= True)

    def set_image_to_default(self):
        self.chat_wallpaper.delete(save=False)  # delete old image file
        self.chat_wallpaper = 'chat_def.jpg'
        self.save()

    def __str__(self) : 
        return self.user.username + "'s profile"
    

class ProfileVerification(models.Model) : 
    profile = models.OneToOneField(Profile, on_delete= models.CASCADE, null= True)
    is_email_verified = models.BooleanField(default= False)
    email_token = models.CharField(max_length= 100, null= True, blank= True)
    forgot_password_token = models.CharField(max_length= 100, null= True, blank= True)

    def __str__(self) : 
        return self.profile.user.username + "'s profile verification"