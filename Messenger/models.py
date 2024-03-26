from django.db import models
from Auth.models import User


# Create your models here.
class Room(models.Model) : 
    name = models.CharField(max_length= 255)
    slug = models.SlugField(unique= True)
    users = models.ManyToManyField(User, blank= True, related_name= 'user_room')

STATUS_CHOICES = (
    ('Online', 'Online'),
    ('Offline', 'Offline'),
    ('Seen', 'Seen')
)

class UserMessages(models.Model) : 
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'users')
    room = models.ForeignKey(Room, on_delete= models.CASCADE, related_name= 'messages')
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add= True)
    pure_date = models.DateField(auto_now= True) # This Is Used For Displaying Messages Per Date
    updated_at = models.DateTimeField(auto_now= True) # Not Important + Not Needed
    status = models.CharField(max_length= 10, choices= STATUS_CHOICES, default= 'Offline')

    class Meta : 
        ordering = ('date_added', )

class Notification(models.Model) : 
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'user_not')
    room = models.ForeignKey(Room, on_delete= models.CASCADE, related_name= 'message_not')
    is_seen = models.BooleanField(default= False)

    def __str__(self) : 
        return self.user.username