# messaging/managers.py

from django.db import models

class UnreadMessagesQuerySet(models.QuerySet):
    """Custom QuerySet for Messages."""
    def unread_for_user(self, user):
        """
        Returns unread messages for a given user.
        The .only() optimization will be applied in the view.
        """
        return self.filter(receiver=user, is_read=False)

class UnreadMessagesManager(models.Manager):
    """Custom Manager for Messages."""
    def get_queryset(self):
        return UnreadMessagesQuerySet(self.model, using=self._db)

    def unread_for_user(self, user):
        """
        Convenience method to call the QuerySet's method.
        Example: Message.unread.unread_for_user(request.user)
        """
        return self.get_queryset().unread_for_user(user)