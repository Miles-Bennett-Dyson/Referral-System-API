from rest_framework import serializers

from users.models import User
from users.services import generate_invite_code


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["__all__"]

    def create(self, validated_data):
        user = User(**validated_data)
        invite_code = generate_invite_code()
        user.invite_code = invite_code
        user.save()
        return user