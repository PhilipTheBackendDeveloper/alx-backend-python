# messaging_app/chats/filters.py

from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    """
    Custom filter set for the Message model.
    
    Allows filtering messages by:
    - The participants in the conversation (using 'user').
    - A specific date range for when the message was sent.
    """
    # Filter to find messages in conversations involving a specific user's username
    user = filters.CharFilter(
        field_name='conversation__participants__username',
        lookup_expr='iexact'
    )
    
    # Filters for a date range
    start_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date', 'conversation']