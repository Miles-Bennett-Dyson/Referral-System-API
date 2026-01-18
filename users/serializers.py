from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User
from users.validators import PhoneFieldValidator


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=12,
        min_length=12,
        help_text="Введите номер телефона, начиная с +79"
    )

    class Meta:
        validators = [
            PhoneFieldValidator()
        ]


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=12,
        min_length=12,
        help_text="Введите номер телефона, начиная с +79"
    )
    sms_code = serializers.IntegerField(
        min_value=1000,
        max_value=9999,
        help_text="Введите цифровой код из смс"
    )

    class Meta:
        validators = [
            PhoneFieldValidator()
        ]


class UserSerializer(serializers.ModelSerializer):
    list_of_referrals = SerializerMethodField()

    def get_list_of_referrals(self, obj):
        return obj.referrals.all().values_list('phone_number', flat=True)

    class Meta:
        model = User
        fields = ("id", "phone_number", "invite_code", "referred_by", "list_of_referrals")


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(
        max_length=6,
        min_length=6,
    )
