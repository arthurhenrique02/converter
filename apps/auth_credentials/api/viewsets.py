from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from .serializers import AuthSerializer


class LoginViewSet(generics.CreateAPIView):
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

        # authenticate user
        user = authenticate(username=username, password=password)

        # check if user`s invalid
        if not user:
            print("INVALID")
            raise ValidationError("Invalid USERNAME or PASSWORD")
    
        # by default, just login

        return Response("logged")
        # return super().create(request, *args, **kwargs)
