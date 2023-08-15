from rest_framework import serializers

from apps.auth_credentials.models import User


class AuthSerializer(serializers.Serializer):

    class Meta:

        model = User

        fields = [
            "id",
            "user",
            "email",
            "password",
        ]
