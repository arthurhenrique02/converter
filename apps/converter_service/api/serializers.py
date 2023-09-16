from rest_framework import serializers

from apps.converter_service.models import Videos


class UploadSerializer(serializers.ModelSerializer):
    class Meta:

        model = Videos

        fields = ["id", "file"]
