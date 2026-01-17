from unittest.mock import patch

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


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

class VerifyCodeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(phone_number="+79277777777")

    def tearDown(self):
        cache.clear()

    def test_verify_code_success(self):
        """ Тест проверки успешного ввода смс-кода """

        url = reverse("users:login")
        phone_number = "+79270879113"
        code = '1234'
        cache.set(f"sms_{phone_number}", code, timeout=60 * 5)

        data = {
            "phone_number": phone_number,
            "sms_code": code
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertTrue(User.objects.filter(phone_number=phone_number).exists())
        self.assertIsNone(cache.get(f"sms_{phone_number}"))

    def test_re_entry(self):
        """ Тест ввода смс-кода уже ранее зарегистрированному пользователю. """

        url = reverse("users:login")
        phone_number = "+79277777777"
        code = '1234'
        cache.set(f"sms_{phone_number}", code, timeout=60 * 5)
        data = {
            "phone_number": phone_number,
            "sms_code": code
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.filter(phone_number=phone_number).count(), 1)

    def test_bad_sms_code(self):
        """ Тест ввода неправильного смс-кода. """

        url = reverse("users:login")
        phone_number = "+79277777777"
        code = '1234'
        cache.set(f"sms_{phone_number}", code, timeout=60 * 5)

        test_cases = [
            ("4321", status.HTTP_400_BAD_REQUEST),
            ("927", status.HTTP_400_BAD_REQUEST),
            ("abc", status.HTTP_400_BAD_REQUEST),
            ("123", status.HTTP_400_BAD_REQUEST),
        ]
        for bad_code, expected_status in test_cases:
            data = {
                "phone_number": phone_number,
                "sms_code": bad_code,
            }
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIsNotNone(cache.get(f"sms_{phone_number}"))
