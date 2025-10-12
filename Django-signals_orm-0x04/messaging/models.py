from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager  


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # Threaded replies
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    # Read/unread tracking
    read = models.BooleanField(default=False)

    # Managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # custom unread manager

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"

    def get_thread(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "receiver": self.receiver.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "replies": [reply.get_thread() for reply in self.replies.all()],
        }


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name="history", on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"
