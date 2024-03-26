from django.urls import path 
from .views import Create, Edit, Delete, Detail, LikePost, Home

urlpatterns = [
    path('', Home, name= 'home'),
    path('create/', Create, name= 'create-post'),
    path('edit/<int:pk>/', Edit, name= 'edit-post'),
    path('delete/<int:pk>/', Delete, name= 'delete-post'),
    path('detail/<int:pk>/', Detail, name= 'detail-post'),
    path('like/<int:pk>/', LikePost, name= 'like_post')
]