from rest_framework import serializers

from users.models import User
from users.services import generate_invite_code
from users.validators import PhoneFieldValidator


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=12,
    )

    class Meta:
        validators = [
            PhoneFieldValidator()
        ]

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "phone_number", "invite_code", "referred_by")

    def create(self, validated_data):
        while True:
            invite_code = generate_invite_code()
            if not User.objects.filter(invite_code=invite_code).exists():
                break
        validated_data["invite_code"] = invite_code
        user = User.objects.create(**validated_data)
        return user
