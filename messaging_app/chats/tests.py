from django.test import TestCase
from .models import CustomUser

class CustomUserModelTest(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpass', role='guest')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'guest')
