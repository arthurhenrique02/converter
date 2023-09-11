from rest_framework import serializers

from apps.converter_service.models import File


class UploadSerializer(serializers.ModelSerializer):
    class Meta:

        model = File

        fields = ["id", "file"]
