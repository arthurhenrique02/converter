from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.converter_service.models import File

from .serializers import UploadSerializer


class UploadViewSet(CreateAPIView, ViewSet):

    queryset = File.objects.all()

    serializer_class = UploadSerializer

    # add authentication and permission
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # Override post
    def create(self, request, *args, **kwargs):

        # try to get file
        try:
            file = request.data["file"]
        except Exception:
            return Response({"message": "Missing file to upload"}, 400)

        # upload file
        uploaded_file = File.objects.create(file=file)

        uploaded_file.save()

        # message that will be sent to rabbitmq
        message = {
            "video_file_id": str(uploaded_file.id),
            "mp3_file_id": None,
            "username": request.data["username"]
        }


class DownloadViewSet(CreateAPIView, ViewSet):
    ...
