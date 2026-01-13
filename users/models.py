from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    password = None

    phone_number = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        unique=True,
    )
    invite_code = models.CharField(
        max_length=6,
        verbose_name="Личный инвайт-код",
        unique=True,
        **NULLABLE,
    )
    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='referrals',
        verbose_name="Кем приглашен",
        **NULLABLE,
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
