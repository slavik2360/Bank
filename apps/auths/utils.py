# Django
from django.conf import settings

# Python
import random
import hashlib
import abc
import secrets


def generate_code(length: int) -> str:
    """
    Создайте случайный код определенной длины.
    
    Код содержит буквы и цифры.
    """
    NUMBERS: str = '1234567890'
    code: str = ''
    for _ in range(length):
        code = code + random.choice(NUMBERS)
    return code


def hash_string(string: str) -> str:
    """
    Hasher, использующий SHA256.
    """
    if string is None:
        raise ValueError("Входная строка не может быть пустой")

    # Генерация соли с использованием secrets
    salt = secrets.token_bytes(32)

    # Создание объекта хеширования с использованием SHA256
    hash_object = hashlib.new('sha256')
    
    # Обновление хеша с учетом соли
    token_with_salt = string.encode('utf-8') + salt
    hash_object.update(token_with_salt)

    # Получение и возвращение хеша в виде строки
    hash_result = hash_object.hexdigest()
    return hash_result


class BaseHasher(metaclass=abc.ABCMeta):
    """
    Абстрактный класс для хеширования строк.
    """
    @abc.abstractmethod
    def hash(self, string: str) -> str:
        pass

class Sha256Hasher(BaseHasher):
    """
    Hasher, использующий SHA256.
    """

    def hash(self, string: str) -> str:
        """
        Хеширует строку с использованием SHA256.
        """
        if string is None:
            raise ValueError("Входная строка не может быть пустой")

        # Генерация соли с использованием secrets
        salt = secrets.token_bytes(32)

        # Создание объекта хеширования с использованием SHA256
        hash_object = hashlib.new('sha256')
        
        # Обновление хеша с учетом соли
        token_with_salt = string.encode('utf-8') + salt
        hash_object.update(token_with_salt)

        # Получение и возвращение хеша в виде строки
        hash_result = hash_object.hexdigest()
        return hash_result
