from django.http import HttpResponse
from .jwt import decode_token
from rest_framework import status


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        applied_routes = ["/search", "/messages", "/contacts", "/status", "user/all", "group/create"]

        # if request.path.contains("/search"):
        if any(applied_route in request.path for applied_route in applied_routes):
            # get authorization header
            auth_header = request.headers.get("Authorization")

            # check if authorization header is present
            if not auth_header or not auth_header.startswith("Bearer "):
                return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

            # extract token from authorization header
            token = auth_header.split(" ")[1]
            data = decode_token(token)
            if not data:
                return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

            request.username = data["username"]
        response = self.get_response(request)
        # Code to be executed for each request/response after the view is called.
        return response
