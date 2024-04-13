# Import necessary modules
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from group.models import Group


# Define the search_usernames view
@api_view(["GET"])
def search_usernames(request):
    # Get the search term from the request
    search_term = request.GET.get("search", "")
    # Get the current user from the request (assuming it is stored in the "username" field)
    current_user = request.username

    if search_term:
        # Filter users whose username contains the search term
        usernames = User.objects.filter(username__icontains=search_term).values_list(
            "username", flat=True
        )
        # Exclude the current user from the list of usernames
        usernames = [username for username in usernames if username != current_user]

        # Filter groups whose name contains the search term
        groupnames = Group.objects.filter(name__icontains=search_term).values_list(
            "name", flat=True
        )
        # Add the group names to the list of usernames
        usernames.extend(groupnames)
    else:
        # If no search term is provided, set usernames to an empty list
        usernames = []

    # Return the list of usernames as a response
    return Response({"usernames": list(usernames)}, status=status.HTTP_201_CREATED)


# Define the get_users view
@api_view(["GET"])
def get_users(request):
    # Get the current user from the request (assuming it is stored in the "username" field)
    current_user = request.username

    # Get all usernames from the User model
    usernames = User.objects.all().values_list("username", flat=True)
    # Exclude the current user from the list of usernames
    usernames = [username for username in usernames if username != current_user]

    # Return the list of usernames as a response
    return Response({"usernames": list(usernames)}, status=status.HTTP_201_CREATED)
