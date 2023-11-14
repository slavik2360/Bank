# Django
from django.utils import timezone

# JWT
from rest_framework_simplejwt.settings import USER_SETTINGS

# Python
from typing import Any
import datetime

# Local
from auths.models import TokenList
from auths.utils import Sha256Hasher


def check_refresh_token_validity(refresh_token: str) -> bool:
    """
    Проверьте, зарегистрирован ли обновление токена в базе данных.
    """
    # Определите Хашер
    hasher: Sha256Hasher = Sha256Hasher()

    # Токен хэш, чтобы проверить его в базе данных
    hashed_refresh_token: str = hasher.hash(refresh_token)

    exists: bool = TokenList.objects.filter(
        refresh_token=hashed_refresh_token).exists()

    return exists


def add_token_to_db(**kwargs: Any) -> None:
    """
    Создайте функцию токена обновления.
    Кваргс должен содержать Пользователя, токен.
    """
    # Получите все токены пользователя
    tokens = TokenList.objects.filter(user=kwargs.get('user')).only('id')

    # Если у пользователя более 4 токенов, удалите их
    if tokens.count() >= 4:
        tokens.delete()

    # Генерировать истечение срока действия DateTime
    datetime_expire: datetime.datetime =\
        timezone.now() + USER_SETTINGS.get('REFRESH_TOKEN_LIFETIME')

    # Определите Хашер
    hasher: Sha256Hasher = Sha256Hasher()
    token: str = kwargs.get('token')

    # Добавить новый токен в базу данных
    TokenList.objects.create(
        user=kwargs.get('user'),
        refresh_token=hasher.hash(token),
        expire_datetime=datetime_expire
    )
