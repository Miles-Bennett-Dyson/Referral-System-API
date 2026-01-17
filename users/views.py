from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, PhoneSerializer, VerifyCodeSerializer, InviteCodeSerializer
from users.services import send_sms_code, verify_and_auth_user, activate_invite_code


class RequestSMSView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            send_sms_code(phone)
            return Response({"message": "Код отправлен"}, status=200)

        return Response(serializer.errors, status=400)

class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            sms_code =  serializer.validated_data['sms_code']
            result = verify_and_auth_user(phone_number=phone, code=sms_code)
            if not result:
                return Response({"error": "Неверный код"}, status=400)

            return Response({
                "access": result['access'],
                "refresh": result['refresh'],
                "invite_code": result['user'].invite_code
            })

        return Response(serializer.errors, status=400)

class ActivateInviteCodeView(APIView):
    def post(self, request):
        serializer = InviteCodeSerializer(data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data['invite_code']
            user = request.user
            activate_invite_code(user, invite_code)
            return Response({"message": "Код активирован"}, status=200)
        return Response(serializer.errors, status=400)

class UserViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
