from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import CreateUserSerializer, PhoneSerializer


class RequestSMSView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            # send_sms_code(phone)
            return Response({"message": "Код отправлен"}, status=200)

        return Response(serializer.errors, status=400)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)

        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    # def get_serializer_class(self):
    #     if self.action == "create":
    #         return CreateUserSerializer
    #     elif self.get_object() == self.request.user:
    #         return UserSerializer
    #     else:
    #         return SecureUserData