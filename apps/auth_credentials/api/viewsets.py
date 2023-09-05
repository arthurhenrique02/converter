from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.auth_credentials.models import User

from .serializers import AuthSerializer


class LoginViewSet(ModelViewSet):
    # add auth
    # authentication_classes = (TokenAuthentication,)

    # add permission
    # permission_classes = (IsAuthenticated,)

    # query
    queryset = User.objects.all()

    # define serializer
    serializer_class = AuthSerializer

    # pagination
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        # get user and password sent
        username = request.data["user"]
        password = request.data["password"]

        # get user
        # user = User.objects.get(user=username)

        user = authenticate(user=username, password=password)
        # check useruser
        if not user:
            print("INVALID")
            return Response("invalid user")
        elif user:
            print("INVALID PASSWORD")
            return Response("Invalid password")

        return Response("logged")
        # return super().create(request, *args, **kwargs)
