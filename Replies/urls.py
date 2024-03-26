from django.urls import path, include 
from .views import LikeReply, Edit, Delete, Create

urlpatterns = [
    path('like/<int:pk>/', LikeReply, name= 'like-reply'),
    path('create/<int:comment_id>/', Create, name= 'create-reply'),
    path('edit/<int:pk>/', Edit, name= 'edit-reply'),
    path('delete/<int:pk>/', Delete, name= 'delete-reply')
]