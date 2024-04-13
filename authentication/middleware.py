
from django.http import HttpResponse
from .jwt import decode_token
from rest_framework import status
from django.http import HttpResponse
from .jwt import decode_token
from rest_framework import status

# Import necessary modules

# Define the JWTAuthMiddleware class
class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # Define the __call__ method
    def __call__(self, request):
        # Define the list of applied routes
        applied_routes = ["/search", "/messages", "/contacts", "/status", "user/all", "group/create"]

        # Check if the request path matches any of the applied routes
        if any(applied_route in request.path for applied_route in applied_routes):
            # Get the authorization header
            auth_header = request.headers.get("Authorization")

            # Check if authorization header is present
            if not auth_header or not auth_header.startswith("Bearer "):
                return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

            # Extract the token from the authorization header
            token = auth_header.split(" ")[1]

            # Decode the token
            data = decode_token(token)

            # Check if the token is valid
            if not data:
                return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

            # Set the username in the request object
            request.username = data["username"]

        # Get the response from the view
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        return response