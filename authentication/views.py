# Import necessary modules
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .serializers import UserSerializer
from .jwt import generate_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .serializers import UserSerializer
from .jwt import generate_token

# Define the signup view
@api_view(["POST"])
def signup(request):
    # Create a new instance of the UserSerializer with the request data
    serializer = UserSerializer(data=request.data)
    # Check if the serializer is valid
    if serializer.is_valid():
        # Save the user object
        serializer.save()
        # Return a success response
        return Response({"message": "OK"}, status=status.HTTP_201_CREATED)
    # Return an error response with the serializer errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define the login view
@api_view(["POST"])
def login(request):
    # Get the username and password from the request data
    username = request.data.get("username")
    password = request.data.get("password")
    try:
        # Try to get a user object with the given username and password
        user = User.objects.get(username=username, password=password)
        # Generate a token for the user
        token = generate_token({"username": user.username})
        # Return the token in a success response
        return Response({"token": token}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        # If the user does not exist, return an error response
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

# Define the logout view
@api_view(["POST"])
def logout(request):
    # You may add any necessary logout logic here, such as revoking tokens or deleting sessions.
    # Return a success response
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
