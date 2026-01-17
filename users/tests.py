from unittest.mock import patch

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SendSmsCodeTestCase(APITestCase):
    def tearDown(self):
        cache.clear()

    @patch('users.services.time.sleep', return_value=None)
    def test_send_sms_code(self, patched_sleep):
        """ Тест успешной отправки смс кода """

        url = reverse("users:request_sms")
        phone_number = "+79270879113"
        data = {
            "phone_number": phone_number
        }
        response = self.client.post(url, data)
        message = response.json()
        code = cache.get(f"sms_{phone_number}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(message.get('message'), "Код отправлен")
        self.assertEqual(len(code), 4)

    def test_wrong_phone_number(self):
        """ Тест ввода неверного номера телефона. """

        url = reverse("users:request_sms")
        test_cases = [
            ("89270879113", status.HTTP_400_BAD_REQUEST),
            ("+7927", status.HTTP_400_BAD_REQUEST),
            ("abc", status.HTTP_400_BAD_REQUEST),
            ("", status.HTTP_400_BAD_REQUEST),
        ]
        for phone, expected_status in test_cases:
            data = {"phone_number": phone}
            response = self.client.post(url, data)
            code = cache.get(f"sms_{phone}")
            self.assertEqual(
                response.status_code,
                expected_status,
                msg=f"Ошибка на номере: {phone}"
            )
            self.assertEqual(code, None)
