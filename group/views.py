from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Group


# Create your views here.
@api_view(["POST"])
def create_group(request):
    data = request.data
    group_name = data.get("groupName")
    usernames = data.get("users")
    usernames.append(request.username)
    Group.create_group(group_name, usernames)
    return Response({"message": "OK"}, status=status.HTTP_200_OK)
