from rest_framework import serializers

from users.models import User
from users.services import generate_invite_code
from users.validators import PhoneFieldValidator


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=12,
        min_length=12
    )

    class Meta:
        validators = [
            PhoneFieldValidator()
        ]

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=12,
        min_length=12
    )
    sms_code = serializers.IntegerField(
        min_value=1000,
        max_value=9999,
        # error_messages="Введенный код имеет неверную длину."
    )
    class Meta:
        validators = [
            PhoneFieldValidator()
        ]

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "phone_number", "invite_code", "referred_by")

class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(
        max_length=6,
        min_length=6,
    )
