# Import necessary modules
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Message
from .serializers import MessageSerializer
from .controllers import get_user_status, get_user_contacts, is_group


# Define a view function to get messages
@api_view(["GET"])
def get_messages(request, target):
    messages = None
    if is_group(target):
        # Get group messages
        messages = Message.get_group_messages(target)
    else:
        # Get user messages
        messages = Message.get_user_messages(request.username, target)
    # Serialize messages
    messages = MessageSerializer(messages, many=True).data
    return Response({"messages": messages}, status=status.HTTP_201_CREATED)


# Define a view function to get contacts
@api_view(["GET"])
def get_contacts(request):
    # Get user contacts
    contacts = get_user_contacts(request.username)
    return Response({"contacts": contacts}, status=status.HTTP_201_CREATED)


# Define a view function to get status
@api_view(["GET"])
def get_status(request):
    # Get user status
    sts = get_user_status(request.username)
    return Response({"status": sts}, status=status.HTTP_200_OK)
