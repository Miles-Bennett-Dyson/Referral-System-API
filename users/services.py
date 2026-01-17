import random
import string
import time

from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


def generate_invite_code():
    """ Генерация уникального 6-значного кода (цифры и буквы) """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=6))


def send_sms_code(phone_number:str):
    """ Имитация отправки смс кода пользователю. """
    time.sleep(random.uniform(1, 2))
    code = str(random.randint(1000, 9999))
    cache.set(f"sms_{phone_number}", code, timeout=60*5)
    print(f"DEBUG: SMS code for {phone_number} is {code}")


def verify_and_auth_user(phone_number, code):
    """Проверка кода и получение/создание пользователя."""

    saved_code = cache.get(f"sms_{phone_number}")

    if not saved_code or saved_code != str(code):
        return None

    user, created = User.objects.get_or_create(phone_number=phone_number)

    if created:
        user.invite_code = generate_invite_code()
        user.save()

    cache.delete(f"sms_{phone_number}")
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': user
    }

def activate_invite_code(user, invite_code:str):

    if user.referred_by:
        raise ValidationError({"invite_code": "Код уже активирован"})

    if user.invite_code == invite_code:
        raise ValidationError({"invite_code": "Вводить свой код нельзя!"})

    inviter = User.objects.filter(invite_code=invite_code).first()
    if not inviter:
        raise ValidationError({"invite_code": "Такой код не найден!"})

    user.referred_by = inviter
    user.save()
