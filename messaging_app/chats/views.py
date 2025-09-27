# chats/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Filter messages by conversation_id in the URL
        and ensure the requesting user is a participant.
        """
        conversation_id = self.kwargs.get("conversation_id")
        conversation = Conversation.objects.filter(id=conversation_id).first()

        if not conversation:
            return Message.objects.none()

        # Enforce that only participants can view
        if self.request.user not in conversation.participants.all():
            return Message.objects.none()

        return Message.objects.filter(conversation=conversation)

    def create(self, request, *args, **kwargs):
        """
        Ensure only participants can send messages in the conversation.
        """
        conversation_id = kwargs.get("conversation_id")
        conversation = Conversation.objects.filter(id=conversation_id).first()

        if not conversation:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant of this conversation."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation, sender=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
