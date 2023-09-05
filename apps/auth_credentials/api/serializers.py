from rest_framework import serializers

from django.contrib.auth.models import User


class AuthSerializer(serializers.Serializer):

    class Meta:
        model = User

        fields = [
            "id",
            "user",
            "email",
            "password",
        ]
