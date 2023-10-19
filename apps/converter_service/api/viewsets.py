import pika
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.converter_service.models import Videos
from apps.converter_service.util.upload import upload

from .serializers import UploadSerializer

# create pika connection
# BlockingConnection is a synchronous adapter
# "rabbitmq" is referencing the rabbitmq host on minikube
# this line is basicaly limiting connection to rabbitmq cluster
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

# create a channel with the connection
channel = connection.channel()


class UploadViewSet(CreateAPIView, ViewSet):

    queryset = Videos.objects.all()

    serializer_class = UploadSerializer

    # add authentication and permission
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    # Override post
    def create(self, request, *args, **kwargs):
        # check files
        if len(request.FILES) != 1:
            return Response(
                {"message": "Exactly one file required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # upload file
        file_upload_status = upload(request=request, channel=channel)

        # return 200 when send to rmq
        return Response(*file_upload_status)


class DownloadViewSet(CreateAPIView, ViewSet):
    ...
