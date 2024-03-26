from django.urls import path,include
from .views import Create, Edit, Delete, LikeComment

urlpatterns = [
    path('create/<int:post_id>/', Create, name='create-comment'),
    path('edit/<int:pk>/', Edit, name= 'edit-comment'),
    path('delete/<int:pk>/', Delete, name= 'delete-comment'),
    path('like/<int:pk>/', LikeComment, name= 'like_comment')
]