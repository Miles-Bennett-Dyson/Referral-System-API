from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, RequestSMSView, VerifyCodeView, ActivateInviteCodeView

app_name = UsersConfig.name

router = DefaultRouter()

urlpatterns = [
    path("login/", VerifyCodeView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path('auth/request_sms/', RequestSMSView.as_view(), name='request_sms'),
    path('user/activate_invite_code/', ActivateInviteCodeView.as_view(), name='activate_invite_code'),
    path('user/', UserViewSet.as_view(), name='user')
] + router.urls
