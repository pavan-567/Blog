from django.db import models
from Posts.models import Post
from Auth.models import User

# Create your models here.
class Comment(models.Model) : 
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    content = models.CharField(max_length= 100)
    updated_at = models.DateTimeField(auto_now= True)
    created_at = models.DateField(auto_now_add= True)

    likes = models.ManyToManyField(User, related_name= 'blog_comments')

    def __str__(self):
        return f"{self.user.username}'s Comment" 
    

    