# in chats/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = 'GUEST', 'Guest'
        HOST = 'HOST', 'Host'
        ADMIN = 'ADMIN', 'Admin' # <-- This is the role we will check for
    
    # ... other fields
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)