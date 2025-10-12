from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Message
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page


@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their account.
    """
    user = request.user
    user.delete()
    return redirect("/")  # redirect to homepage or login page after deletion

@login_required
def conversation_list(request):
    """
    Retrieve all top-level messages and their threaded replies.
    Optimized with select_related and prefetch_related.
    """
    messages = (
        Message.objects.filter(receiver=request.user) 
        .select_related("sender", "receiver")         
        .prefetch_related("replies__sender", "replies__receiver") 
    )

    data = [message.get_thread() for message in messages]
    return JsonResponse(data, safe=False)


@login_required
def send_message(request, receiver_id):
    """
    Example view for sending a new message (to show sender=request.user).
    """
    from django.contrib.auth.models import User
    import json

    if request.method == "POST":
        body = json.loads(request.body)
        receiver = get_object_or_404(User, id=receiver_id)
        parent_message_id = body.get("parent_message")

        parent_message = None
        if parent_message_id:
            parent_message = get_object_or_404(Message, id=parent_message_id)

        message = Message.objects.create(
            sender=request.user,               
            receiver=receiver,                  
            content=body["content"],
            parent_message=parent_message,
        )

        return JsonResponse({"id": message.id, "content": message.content})

    return JsonResponse({"error": "Invalid request"}, status=400)

def unread_inbox(request):
    # Use the custom manager
    unread_messages = (
        Message.unread.unread_for_user(request.user)
        .only("id", "sender", "receiver", "content", "timestamp")
    )

    return render(request, "messaging/unread_inbox.html", {"messages": unread_messages})

@cache_page(60) 
def conversation(request, username):
    """View to display a conversation between the logged-in user and another user"""
    receiver = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by("timestamp")

    return render(request, "chats/conversation.html", {
        "messages": messages,
        "receiver": receiver,
    })
