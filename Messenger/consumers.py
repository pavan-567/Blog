import json 

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Room, UserMessages, Notification
from Auth.models import User
from Profile.models import Profile
from django.urls import reverse

class ChatConsumer(AsyncWebsocketConsumer) : 
    async def connect(self) : 
        my_id = self.scope['user'].id
        other_id = self.scope['url_route']['kwargs']['id']

        if int(my_id) > int(other_id) : 
            self.room_name = f'{my_id}-{other_id}'
        else : 
            self.room_name = f'{other_id}-{my_id}'


        self.room_group_name = f'chat-{self.room_name}'
        print(self.room_name, self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None): 
        data = json.loads(text_data)
        message = data['message']
        username = data['name']
        email = data['mail']
        room = data['room']
        receiver = data['receiver']

        await self.save_message(username, email, room, message, receiver)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message' : message,
                'username': username,
                'email': email,
                'room' : room
            }
        )

    async def disconnect(self, code= None) : 
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.send(text_data= {'msg': 'disconnected'})
    
    async def chat_message(self, event) : 
        message = event['message']
        username = event['username']
        email = event['email']
        room = event['room']

        image_url = await self.ImageURL(email)

        await self.send(text_data= json.dumps({
            'message': message,
            'username': username,
            'room': room,
            'image_url': image_url
        }))
    
    @sync_to_async
    def ImageURL(self, email) : 
        user = User.objects.get(email= email)
        return user.profile.image.url

    @sync_to_async
    def save_message(self, username, email, room, message, receiver) : 
        user = User.objects.get(email= email)
        room = Room.objects.get(slug= room)
        msgs = UserMessages.objects.create(user= user, room= room, content= message)
        get_other_user = User.objects.get(id= self.scope['url_route']['kwargs']['id'])
        print("From Chat Consumer => " , receiver, get_other_user.username, "OTHER ID : => ", self.scope['url_route']['kwargs']['id'])
        Notification.objects.create(room= room, user= get_other_user)




class OnlineConsumer(AsyncWebsocketConsumer) : 
    active_users = []
    async def connect(self):
        self.room_name = 'user'
        self.room_group_name = f'chat-{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
    
        await self.accept()

    
    async def receive(self, text_data=None, bytes_data=None): 
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']

        await self.change_online_status(username, connection_type)

    
    @database_sync_to_async
    def change_online_status(self, username, c_type) : 
        user = User.objects.get(username= username)
        profile = Profile.objects.get(user= user)
        if c_type == 'open' : 
            profile.status = True
            self.active_users.append(username) 
            profile.save()
        else : 
            profile.status = False 
            self.active_users.remove(username)
            profile.save()
        print(user, profile, profile.status)

    async def Send_OnlineStatus(self, event) : 
        print("I AM INSIDE SEND STATUS!")
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']

        all_users = await self.get_all_users()

        await self.send(text_data= json.dumps({
            'username': username,
            'online_status': online_status,
            'users': list(set(self.active_users)),
            'all_users': all_users
        }))

    @sync_to_async
    def get_all_users(self) : 
        all_users = []
        for user in User.objects.filter(profile__profileverification__is_email_verified= True) : 
            di = {}
            di['username'] = user.username
            di['imageURL'] = user.profile.image.url 
            di['profileLink'] = reverse('profile', kwargs= {'pk': user.profile.id})

            if user.username in self.active_users : 
                di['active'] = True
            else : 
                di['active'] = False 

            all_users.append(di)
        return all_users


    async def disconnect(self, code):
        print("DISCONNECTED!")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.send(text_data= {'msg': 'disconnected'})


class NotificationConsumer(AsyncWebsocketConsumer) : 
    async def connect(self) : 
        id = self.scope['user'].id
        self.room_group_name = f'{id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        
    
    async def send_notification(self, event) : 
        data = json.loads(event.get('value'))
        count = data['count']
        await self.send(text_data= json.dumps({'count': count}))

    async def disconnect(self, code) : 
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )