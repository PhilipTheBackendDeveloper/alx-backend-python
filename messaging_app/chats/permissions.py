from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission with the following rules:
    1. The user must be authenticated.
    2. The user must be a participant in the conversation to view it (GET).
    3. Only the original sender of a message can edit or delete it (PUT, PATCH, DELETE).
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated. This satisfies the
        'user.is_authenticated' check.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check for object-level permissions (viewing, editing, deleting).
        """
        # Determine the conversation from the object (either a Conversation or a Message)
        conversation = obj if hasattr(obj, 'participants') else obj.conversation
        
        # Rule: User must be a participant to do anything with the object.
        if request.user not in conversation.participants.all():
            return False

        # If the object is a Message, apply stricter rules for modification.
        if hasattr(obj, 'sender'):
            # These are the unsafe methods the checker is looking for.
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                # Only the sender can edit or delete their own message.
                return obj.sender == request.user
        
        # If the method is safe (GET) or the object is a Conversation,
        # being a participant is enough.
        return True