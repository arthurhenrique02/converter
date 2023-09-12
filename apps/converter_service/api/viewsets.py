import pika
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.converter_service.models import File
from apps.converter_service.util.upload import upload
from converter.rmq_server import channel

from .serializers import UploadSerializer


class UploadViewSet(CreateAPIView, ViewSet):

    queryset = File.objects.all()

    serializer_class = UploadSerializer

    # add authentication and permission
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    # Override post
    def create(self, request, *args, **kwargs):

        # check files
        if len(request.data["file"]) != 1:
            return Response({"message": "Exactly one file required"}, 400)

        # upload file
        file_upload_status = upload(request=request, channel=channel)

        # return 200 when send to rmq
        return Response({"message": "success"}, 200)


class DownloadViewSet(CreateAPIView, ViewSet):
    ...
