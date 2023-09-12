from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import AuthSerializer


class LoginViewSet(CreateAPIView, ViewSet):
    # define serializer
    serializer_class = AuthSerializer

    # override POST method to get login credentials
    def create(self, request, *args, **kwargs):
        # get user and password sent
        try:
            username = request.data["username"]
            password = request.data["password"]
        except Exception:
            return Response(
                {"message": "Missing credentials (username or password)"}
            )

        # authenticate user
        user = authenticate(username=username, password=password)

        # check if user`s invalid
        if not user:
            return Response({"message": "Invalid USERNAME or PASSWORD"}, 404)

        # by default, just login
        return Response({"message": "Logged in"}, 202)


class LogoutViewSet(CreateAPIView, ViewSet):
    # define serializer
    serializer_class = AuthSerializer

    # override POST method to just logout
    def create(self, request, *args, **kwargs):
        logout(request=request)

        # by default, just login
        return Response({"message": "Logged out"}, 200)


class CreateUserViewSet(CreateAPIView, ViewSet):
    # define serializer
    serializer_class = AuthSerializer

    # override POST
    def create(self, request, *args, **kwargs):
        # get user and password sent
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]

        # check sent credentials
        if not username:
            return Response({"message": "Missing user"}, 404)

        if not email:
            return Response({"message": "Missing email"}, 404)

        if not password:
            return Response({"message": "Missing password"}, 404)

        # create and save new user instance
        new_user = User.objects.create(
            username=username
        )
        new_user.set_password(password)
        new_user.email = email
        new_user.save()

        return Response({"message": "User created"}, 201)
