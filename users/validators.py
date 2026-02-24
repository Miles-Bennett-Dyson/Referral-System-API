import re

from rest_framework.serializers import ValidationError


class PhoneFieldValidator:
    """ Проверяет телефон на соответствие формату """

    def __call__(self, phone_number):
        format_pattern = r'^\+79\d{9}$'
        numbers = re.match(format_pattern, phone_number)
        if not numbers:
            raise ValidationError("Телефон не соответствует формату: +79XXXXXXXXX")
