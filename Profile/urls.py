from django.urls import path 
from .views import Edit, Profile_Follow_Unfollow

urlpatterns = [
    path('Edit/', Edit, name= 'edit-profile'),
    path('<int:pk>/', Profile_Follow_Unfollow, name= 'profile')
]