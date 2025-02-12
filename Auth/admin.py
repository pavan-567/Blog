from django.contrib import admin
from .models import User

from django.contrib.sessions.models import Session
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

# Register your models here.
admin.site.register(User)
admin.site.register(Session, SessionAdmin)