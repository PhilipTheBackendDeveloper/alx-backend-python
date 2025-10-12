#!/usr/bin/env python3
"""Serializers for chats app with nested relationships and custom validation."""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with explicit fields."""

    # Explicitly declare some fields
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with computed field."""

    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender_name",
            "message_body",
            "sent_at",
        ]

    def get_sender_name(self, obj):
        """Return sender full name as a computed field."""
        return f"{obj.sender.first_name} {obj.sender.last_name}"


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages and validation."""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source="message_set")

    title = serializers.CharField(required=False)  # Example explicit field

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
            "title",
        ]

    def validate_title(self, value):
        """Custom validation to disallow empty titles if provided."""
        if value is not None and value.strip() == "":
            raise serializers.ValidationError("Title cannot be empty.")
        return value
