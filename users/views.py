from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, PhoneSerializer, VerifyCodeSerializer, InviteCodeSerializer
from users.services import send_sms_code, verify_and_auth_user, activate_invite_code


class RequestSMSView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Запрос СМС-кода на указанный номер",
        request_body=PhoneSerializer,
        responses={200: '{"message": "Код отправлен"}', 400: 'Ошибка валидации'}
    )
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            send_sms_code(phone)
            return Response({"message": "Код отправлен"}, status=200)

        return Response(serializer.errors, status=400)


class VerifyCodeView(APIView):

    @swagger_auto_schema(
        operation_description="Подтверждение смс-кода и авторизация и/или создание нового пользователя.",
        request_body=VerifyCodeSerializer,
        responses={200: '{"access": "access-token",  "refresh": "refresh-token", "invite_code": "user-invite_code"}',
                   400: 'Ошибка валидации'}
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            sms_code = serializer.validated_data['sms_code']
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

    @swagger_auto_schema(
        operation_description="Активация инвайт-кода пользователем.",
        request_body=InviteCodeSerializer,
        responses={200: '{"message": "Код активирован"}', 400: 'Ошибка валидации'}
    )
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
    operation_summary = "Профиль текущего пользователя"

    def get_object(self):
        return self.request.user


class RequestSMSTemplateView(TemplateView):
    template_name = "users/phone_input.html"


class VerifyCodeTemplateView(TemplateView):
    template_name = "users/code_verify.html"


class ProfileTemplateView(TemplateView):
    template_name = 'users/profile.html'
