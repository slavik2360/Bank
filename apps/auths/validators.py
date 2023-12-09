# Django
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.conf import settings

# Python
import re
from typing import Union, Literal

# Local
from .models import (
    User,
    AccountCode,
    TokenList
)
from auths.utils import Sha256Hasher


def email_validation_error(
    email: str,
    find_user: bool = False,
    allowed_domains: list = settings.ALLOWED_DOMAINS,
    raise_exception: bool = False
) -> dict:
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Проводим валидацию электронной почты
    match = pattern.match(email)
    error = {'email': []}

    if not match:
        error['email'].append('Электронная почта должна начинаться с буквы \
                              и содержать не менее двух символов в основной части.')
    elif match.group(0).split('@')[1] not in allowed_domains:
        error['email'].append(f'Домен {match.group(0).split("@")[1]} не разрешен.')
    else:
        # Если флаг find_user включен, проверяем наличие пользователя
        if find_user:
            user = User.objects.get_object_or_none(email=email)
            if user is None:
                error = {'email': ['Пользователь с таким email не найден.']}
            elif not user.is_active:
                error = {'email': ['Пользователь неактивен.']}
    
    # Если есть ошибки и флаг raise_exception включен, вызываем исключение
    if error.get('email') and raise_exception:
        raise ValidationError(error)

    # Возвращаем ошибки или None
    return error if error.get('email') else None


def password_validation_error(password1: str,
                              password2: str = None,
                              user: User = None,
                              raise_exception: bool = False
                              ) -> dict | None:
    """
    Возвращает ошибки, если пароли не соответствуют критериям.
    Критерии:
    * Новый пароль не должен совпадать с предыдущим.
    * Длина пароля должна быть не менее 7 символов.
    * Пароль должен содержать буквы и цифры.
    * Пароль1 должен совпадать с паролем2.

    Возвращает словарь ошибок или None.
    """
    error: dict = {'password': []}

    # Проверка, совпадает ли новый пароль с предыдущим
    if user and user.is_authenticated and user.check_password(password1):
        error['password'].append('Пароль не должен совпадать с предыдущим.')

    # Проверка, что длина пароля менее 7 символов
    if len(password1) < 7:
        error['password'].append('Длина пароля должна быть не менее 7 символов.')

    # Проверка, что пароль содержит буквы и цифры
    if not password1.isalnum():
        error['password'].append('Пароль должен содержать буквы и цифры.')

    # Проверка, что пароль1 не совпадает с паролем2
    if password2 and password1 != password2:
        error['password'].append('Несоответствие паролей.')
        error.update({'password2': ['Несоответствие паролей.']})

    # Если есть ошибки и флаг raise_exception включен, вызвать исключение
    if error['password'] and raise_exception:
        raise ValidationError(error)

    # Возврат ошибок или None
    return error['password'] or None


def login_data_validation_error(email: str, password: str, user: User,
                                raise_exception: bool = False
                                ) -> dict | None:
    """
    Возвращает ошибку, если данные для входа в систему недействительны. 
    Проверяет, если электронная почта и пароль не пусты, 
    и пользователь аутентифицирован.
    """
    error: dict = {}

    # Если электронная почта пуста
    if not email:
        error.update({'email': ['Это поле обязательно для заполнения.']})

    # Если пароль пуст
    if not password:
        error.update({'password': ['Это поле обязательно для заполнения.']})

    # Если пользователь не найден, а электронная почта и пароль указаны
    if user is None and email and password or not user.is_active:
        error.update({'email': ['Проверьте email или пароль.']})
        error.update({'password': ['Проверьте email или пароль.']})


    # Если есть ошибки и флаг raise_exception включен, вызвать исключение
    if error and raise_exception is True:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None


def is_email_confirmed(email: str, raise_exception: bool = False
                       ) -> Union[dict, User, Literal['update', 'create']]:
    """
    Проверяет, завершена ли подтверждение электронной почты пользователя
    или доступна новая авторизация.
    ---
    * если найден активный пользователь
    Возвращает ошибку.
    ---
    * Если raise_exceptions равен True
    Вызывает ошибки.
    ---
    * Если активный пользователь не найден
    Возвращает 'update'.
    ---
    * Если пользователь не найден, возвращает 'create'.
    Возвращает 'create'.
    """
    error: dict = {}

    user: User | None
    if user := User.objects.get_object_or_none(email=email):

        # Если пользователь уже подтвержден
        if user.is_active:
            error: dict = {'email': ['Пользователь с этим адресом электронной почты уже существует.']}

        # Определяем, что мы должны обновить пользователя
        else:
            return 'update'
    # Определяем, что мы должны создать пользователя
    else:
        return 'create'

    # Если есть ошибки и флаг raise_exception включен, вызвать исключение
    if raise_exception is True:
        if error:
            raise ValidationError(error)
        return user
    
    # Возвращаем ошибки
    return error


def user_code_validation(user: User, code: str, code_type: int,
                         raise_exception: bool = False) -> dict | None:
    """
    Найти пользователя и проверить, не истек ли срок действия кода.
    Пользователь с этим адресом электронной почты должен быть неактивным,
    код должен быть не истекшим и принадлежать пользователю.
    Возвращает словарь ошибок или None.
    """
    error: dict = {}

    # Ищет код с действительным сроком жизни и соответствующий пользователю
    activation_code: QuerySet[AccountCode] =\
        AccountCode.objects.extended_filter(user=user, expired=False,
                                            code=code, code_type=code_type)

    # Проверка, существуют ли такие коды
    if activation_code.exists() is False:
        error.update({'code': ['Этот код недействителен.']})

    # Если пользователя нет, должна возникнуть только ошибка о том, что пользователь не найден
    if user is None:
        error = {'email': ['Пользователь с таким адресом электронной почты не найден.']}

    # Если пользователь активен, должна возникнуть только ошибка
    # о том, что пользователь уже подтвержден
    elif user.is_active and code_type == AccountCode.ACCOUNT_ACTIVATION:
        error = {'email': ['Пользователь с таким адресом электронной почты уже подтвержден.']}

    # Если есть ошибки и флаг raise_exception включен, вызвать исключение
    if raise_exception is True:
        if error:
            raise ValidationError(error)
        return activation_code.last()

    # Вернуть ошибки или None
    return error if error else None


def old_password_validation_error(user: User, password: str,
                                  raise_exception: bool = False
                                  ) -> dict | None:
    """
    Проверяет, является ли указанный пароль старым паролем пользователя.
    Возвращает словарь ошибок или None.
    """
    error: dict = {}

    # Проверка, если старый пароль не действителен
    if not user.check_password(password):
        error = {'old_password': ['Старый пароль недействителен.']}

    # Если есть ошибки и флаг raise_exception включен, вызвать исключение
    if error and raise_exception is True:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None

def refresh_token_validation_error(token: str,
                                   raise_exception: bool = False
                                   ) -> dict | None:
    """
    Проверяет валидность refresh token.

    Возвращает словарь ошибок или None.
    """
    error: dict = {}

    # Определение хэшера
    hasher: Sha256Hasher = Sha256Hasher()

    # Проверка, является ли refresh token действительным
    token: str = hasher.hash(token)
    token: TokenList =\
        TokenList.objects.find_valid(token=token).last()

    # Если не действительный и функция должна вызвать исключение
    if not token and raise_exception is True:
        error: dict = {
            'refresh': ['Refresh token не является действительным.']
        }
        raise ValidationError(error)

    return error if error else None





