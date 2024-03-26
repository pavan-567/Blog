from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
import json

@receiver(post_save, sender= Profile)
def Send_OnlineStatus(sender, instance, created, **kwargs) : 
    if not created : 
        channel_layer = get_channel_layer()
        user = instance.user.username
        user_status = instance.status 

        data = {
            'username': user,
            'status': user_status
        }

        async_to_sync(channel_layer.group_send)(
            'chat-user', {
                'type': 'Send_OnlineStatus',
                'value': json.dumps(data)
            }
        )