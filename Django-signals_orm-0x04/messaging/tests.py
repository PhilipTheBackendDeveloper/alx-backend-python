from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

# Get the active User model
User = get_user_model()

class SignalTestCase(TestCase):
    """
    Test suite to verify that Django signals are working correctly.
    """

    def setUp(self):
        """
        Set up two users for testing purposes before each test.
        """
        self.user_sender = User.objects.create_user(username='sender', password='password123')
        self.user_receiver = User.objects.create_user(username='receiver', password='password123')

    def test_notification_is_created_when_new_message_is_saved(self):
        """
        Tests that a Notification is automatically created via a post_save signal
        when a new Message instance is created and saved.
        """
        # 1. Verify that no notifications exist at the start of the test.
        self.assertEqual(Notification.objects.count(), 0)
        
        # 2. Create a new message. This action should trigger the post_save signal.
        message = Message.objects.create(
            sender=self.user_sender,
            receiver=self.user_receiver,
            content="Hello, this is a test message!"
        )
        
        # 3. Verify that exactly one notification has been created in the database.
        self.assertEqual(Notification.objects.count(), 1)
        
        # 4. Verify that the created notification is correct.
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user_receiver) # It's for the receiver.
        self.assertEqual(notification.message, message) # It's linked to the correct message.
        self.assertFalse(notification.is_read) # It should be unread by default.