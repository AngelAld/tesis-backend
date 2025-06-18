from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to handle JWT authentication for WebSocket connections.
    """

    async def __call__(self, scope, receive, send):
        # Extract the token from the query parameters or headers
        token = self.get_token(scope)

        if token:
            user = await self.get_user_from_token(token)
            scope["user"] = user
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def get_token(self, scope):
        # Check for token in query parameters
        if "query_string" in scope:
            query_string = scope["query_string"].decode()
            params = {}
            for param in query_string.split("&"):
                if "=" in param:
                    k, v = param.split("=", 1)
                    params[k] = v
            return params.get("token")

        # Check for token in headers
        for header in scope.get("headers", []):
            if header[0] == b"authorization":
                return header[1].decode().split(" ")[1]  # Bearer token

        return None

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            from rest_framework.request import Request
            from django.test.client import RequestFactory

            # Create a DRF Request with the token in the headers
            factory = RequestFactory()
            django_request = factory.get("/", HTTP_AUTHORIZATION=f"Bearer {token}")
            drf_request = Request(django_request)
            auth_result = JWTAuthentication().authenticate(drf_request)
            if auth_result is not None:
                user, _ = auth_result
                return user
            return AnonymousUser()
        except (InvalidToken, TokenError):
            return AnonymousUser()  # Return AnonymousUser if token is invalid
