from django.contrib import admin
from .models import Profile, ProfileVerification

# Register your models here.
class ProfileAdmin(admin.ModelAdmin) : 
    readonly_fields = ('updated_at',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileVerification)