#!/usr/bin/env python3
"""Routes for chats app."""

from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Use NestedDefaultRouter for proper structure
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

# Nested router: messages belong to a conversation
conversations_router = routers.NestedDefaultRouter(router, r"conversations", lookup="conversation")
conversations_router.register(r"messages", MessageViewSet, basename="conversation-messages")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversations_router.urls)),
]
