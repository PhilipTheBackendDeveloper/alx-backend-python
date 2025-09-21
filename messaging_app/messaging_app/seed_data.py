# chat/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import Message
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with users and messages.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Message.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        fake = Faker()
        self.stdout.write("Creating new users...")
        user1 = User.objects.create_user('alice', 'alice@example.com', 'password123')
        user2 = User.objects.create_user('bob', 'bob@example.com', 'password123')
        
        self.stdout.write("Creating new messages...")
        Message.objects.create(sender=user1, receiver=user2, content=fake.sentence())
        Message.objects.create(sender=user2, receiver=user1, content=fake.sentence())

        self.stdout.write(self.style.SUCCESS('Database has been seeded!'))