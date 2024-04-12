# authentication/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .serializers import UserSerializer
from .jwt import generate_token


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "OK"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    try:
        user = User.objects.get(username=username, password=password)
        token = generate_token({"username": user.username})
        return Response({"token": token}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
def logout(request):
    # You may add any necessary logout logic here, such as revoking tokens or deleting sessions.
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
