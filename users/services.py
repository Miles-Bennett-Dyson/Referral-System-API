import random
import string


def generate_invite_code():
    """Генерация уникального 6-значного кода (цифры и буквы)"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=6))
