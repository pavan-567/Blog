from django.db import models
from Comments.models import Comment 
from Auth.models import User

# Create your models here.
class Reply(models.Model) : 
    comment = models.ForeignKey(Comment, related_name= 'replies', on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    reply = models.TextField()

    likes = models.ManyToManyField(User, related_name= 'like_reply')

    def __str__(self) : 
        return f'{self.user.username}\'s Reply'
    
    @property
    def get_replies(self) : 
        return self.replies.all()