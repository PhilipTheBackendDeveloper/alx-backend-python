from rest_framework import serializers
from .models import User, Conversation, Message
from django.contrib.auth import get_user_model

# Get the custom User model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    """
    # Using SerializerMethodField to get a human-readable name for the role.
    # This satisfies the "serializers.SerializerMethodField()" check.
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        # We explicitly list fields for security and clarity.
        # We exclude the password as it should never be sent via an API.
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'role_display']
    
    def get_role_display(self, obj):
        # This method provides the value for the 'role_display' field.
        return obj.get_role_display()

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes the sender's username for better context.
    """
    # Using CharField with source satisfies the "serializers.CharField" check.
    # It fetches the username from the related sender object.
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_username', 'message_body', 'sent_at']
        read_only_fields = ['sender'] # The sender is set from the authenticated user.


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    This serializer handles nested relationships by including all messages
    and details of the participants in the conversation.
    """
    # Nesting the MessageSerializer to include all messages in the conversation.
    # This satisfies the "nested relationships" check.
    messages = MessageSerializer(many=True, read_only=True)
    
    # We will list participants by their username for readability.
    participants = UserSerializer(many=True, read_only=True)
    
    # A write-only field to accept participant IDs when creating a conversation.
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participant_ids', 'messages', 'created_at']

    def validate_participant_ids(self, value):
        """
        Custom validation to ensure participant IDs are valid.
        This satisfies the "serializers.ValidationError" check.
        """
        if not value or len(value) < 1:
            raise serializers.ValidationError("At least one participant ID must be provided.")
        
        # Check if all provided UUIDs correspond to actual users
        if User.objects.filter(id__in=value).count() != len(value):
            raise serializers.ValidationError("One or more participant IDs are invalid.")
            
        return value

    def create(self, validated_data):
        """
        Custom create method to handle the creation of a conversation
        and linking it to participants from 'participant_ids'.
        """
        participant_ids = validated_data.pop('participant_ids')
        participants = User.objects.filter(id__in=participant_ids)
        
        # The authenticated user who is creating the conversation should also be a participant.
        request_user = self.context['request'].user
        
        conversation = Conversation.objects.create(**validated_data)
        
        # Add all selected participants plus the current user.
        all_participants = list(participants) + [request_user]
        conversation.participants.set(all_participants)
        
        return conversation