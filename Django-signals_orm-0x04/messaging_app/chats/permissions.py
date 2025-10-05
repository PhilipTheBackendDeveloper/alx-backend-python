from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own conversations/messages.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming your Message model has a `sender` field
        # and Conversation model has a `participants` relation
        if hasattr(obj, 'sender'):  
            return obj.sender == request.user
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users who are participants in a conversation
    to send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if user is a participant in the conversation
        if hasattr(obj, "conversation"):  # Message object
            conversation = obj.conversation
        else:  # Conversation object
            conversation = obj

        # Allow safe methods (GET, HEAD, OPTIONS) only if participant
        if request.method in permissions.SAFE_METHODS:
            return request.user in conversation.participants.all()

        # Explicitly check for write methods
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user in conversation.participants.all()

        return False