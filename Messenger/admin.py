from django.contrib import admin
from .models import Room, UserMessages, Notification
# Register your models here.
class UserMessagesAdmin(admin.ModelAdmin) : 
    readonly_fields = ('updated_at',)

admin.site.register(Room)
admin.site.register(UserMessages, UserMessagesAdmin)
admin.site.register(Notification)