from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender= Notification)
def send_notification(sender, instance, created, **kwargs) : 
    if created : 
        channel_layer = get_channel_layer()
        notifications = Notification.objects.filter(is_seen= False, user= instance.user).count()
        data = {
            'count': notifications,
        }
        id = str(instance.user.id)
        print("NOTIFICATION GOT CREATED!")

        async_to_sync(channel_layer.group_send)(
            id, {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )
        