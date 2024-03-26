from django.urls import path
from .consumers import ChatConsumer, OnlineConsumer, NotificationConsumer

ws_urlpatterns = [
    path('ws/status/', OnlineConsumer.as_asgi()),
    path('ws/<int:id>/', ChatConsumer.as_asgi()),
    path('ws/notify/', NotificationConsumer.as_asgi())
]