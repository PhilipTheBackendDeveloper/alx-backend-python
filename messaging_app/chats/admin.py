from django.contrib import admin
from .models import Message, Conversation, CustomUser

# Register your models for the admin interface
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(CustomUser)
