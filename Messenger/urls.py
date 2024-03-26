from django.urls import path 

from .views import MessageRoom, ChangeChatWallpaper, SetDefaultChatWallpaper


urlpatterns = [
    path('<int:pk>/', MessageRoom, name= 'message'),
    path('chat-wallpaper/<int:receiver_pk>/', ChangeChatWallpaper, name= 'chat-wallpaper'),
    path('default-wallpaper/<int:receiver_pk>/', SetDefaultChatWallpaper, name= 'default-wallpaper')
]