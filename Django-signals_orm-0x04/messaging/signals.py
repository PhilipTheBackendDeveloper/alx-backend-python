from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving a Message, check if it's being updated.
    If so, save the old content into MessageHistory.
    """
    if instance.id:  # existing message (not new)
        try:
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:  # content actually changed
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.sender  # tracks who edited
                )
                instance.edited = True  # mark as edited
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    """
    When a user is deleted, clean up related messages, notifications, and histories.
    """
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories where the user was the editor
    MessageHistory.objects.filter(edited_by=instance).delete()