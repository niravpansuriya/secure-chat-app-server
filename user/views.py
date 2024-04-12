from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from group.models import Group


# Create your views here.
@api_view(["GET"])
def search_usernames(request):
    search_term = request.GET.get("search", "")
    current_user = request.username
    if search_term:
        usernames = User.objects.filter(username__icontains=search_term).values_list(
            "username", flat=True
        )
        usernames = [username for username in usernames if username != current_user]
        groupnames = Group.objects.filter(name__icontains=search_term).values_list(
            "name", flat=True
        )
        usernames.extend(groupnames)
    else:
        usernames = []
    return Response({"usernames": list(usernames)}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_users(request):
    current_user = request.username
    usernames = User.objects.all().values_list("username", flat=True)
    usernames = [username for username in usernames if username != current_user]
    return Response({"usernames": list(usernames)}, status=status.HTTP_201_CREATED)
