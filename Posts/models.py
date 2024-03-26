from django.db import models
from Auth.models import User
from Category.models import Category

# Create your models here.
class Post(models.Model) : 
    title = models.CharField(max_length= 100)
    image = models.ImageField(upload_to= 'posts', null= True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add= True)
    date_updated = models.DateTimeField(auto_now= True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    likes = models.ManyToManyField(User, related_name= 'blog_posts')
    slug = models.SlugField(max_length= 200, null= True)

    class Meta : 
        ordering = ('-date_created',)

    def __str__(self) : 
        return self.title