from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class AuthViewSet(ModelViewSet):
    # add auth
    authentication_classes = (TokenAuthentication,)

    # add permission
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # get user and password sent
        user = request.data["user"]
        password = request.data["password"]

        return super().create(request, *args, **kwargs)
