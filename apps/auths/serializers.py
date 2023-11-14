# Django
# DRF
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import serializers

# Simple JWT
from rest_framework_simplejwt.tokens import RefreshToken

# Python
import datetime

# Local
from abstracts.mixins import AccessTokenMixin
from abstracts.serializers import CustomValidSerializer
from auths.models import (
    User,
    AccountCode,
    TokenList,
)
from auths.utils import generate_code
from auths.services.token_utils import add_token_to_db
from auths.validators import (
    is_email_confirmed,
    email_validation_error,
    password_validation_error,
    login_data_validation_error,
    user_code_validation,
    refresh_token_validation_error,
    password_recovery_validation_error,
    old_password_validation_error,
)


class RegistrateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя для регистрации.
    """

    email: str = serializers.CharField(max_length=60, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'password', 'password2', 'gender')

    def validate(self, attrs: dict) -> dict:
        """Валидация данных."""
        email: str = attrs.get('email')
        password: str = attrs.get('password')
        password2: str = attrs.get('password2')

        # Проверка, является ли электронная почта действительной
        email_validation_error(email=email, raise_exception=True)

        # Проверка, являются ли пароли действительными
        password_validation_error(password1=password, password2=password2, raise_exception=True)

        # Проверка, подтвержден ли пользователь
        status: str = is_email_confirmed(email=email, raise_exception=True)

        # Используется затем в .save()
        self.status = status
        return attrs

    def save(self) -> None:
        """
        Сохранение пользователя с деактивацией учетной записи и хешированием пароля.
        """
        email: str = self.validated_data.get('email')
        first_name: str = self.validated_data.get('first_name')
        last_name: str = self.validated_data.get('last_name')
        password: str = self.validated_data.get('password')
        user: User | None = User.objects.get_object_or_none(email=email)

        if user:
            # Если пользователь уже существует
            user.first_name = first_name
            user.last_name = last_name
            user.password = password
            user.set_password(password)
            user.password2 = user.password
            user.save()
        else:
            # Если пользователь регистрируется впервые
            user: User = User.objects.create(**self.validated_data)

        # Используется для улучшения читаемости кода
        code_type: int = AccountCode.ACCOUNT_ACTIVATION
        code_length: int = AccountCode.CODE_LENGTH

        # Создание нового кода активации учетной записи
        AccountCode.objects.create(user=user, code=generate_code(code_length), code_type=code_type)

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': 'Подтвердите свою учетную запись. Код был отправлен на вашу почту.'
        }
        return response


class LoginUserSerializer(CustomValidSerializer):
    """
    Сериализатор пользователя для входа в систему.
    """
    email: str = serializers.CharField(max_length=60, required=True)
    password: str = serializers.CharField(max_length=128, required=True)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        email: str = attrs.get('email')
        password: str = attrs.get('password')

        # Попытка аутентификации пользователя
        user: User | None = authenticate(email=email, password=password)

        # Проверка, разрешено ли пользователю входить в систему
        login_data_validation_error(email=email, password=password, user=user, raise_exception=True)

        # Установка атрибута .user для использования его в .save()
        self.user = user

        return attrs

    def save(self) -> None:
        """
        Генерация refresh и access токенов.
        """
        user: User = self.user

        # Генерация пары токенов и создание
        # атрибута .refresh для использования в .get_response()
        refresh: RefreshToken = RefreshToken.for_user(user)

        # Добавление refresh токена в базу данных
        add_token_to_db(user=user, token=str(refresh))

        # Установка атрибута .is_refresh для использования его в .get_response()
        self.refresh = refresh

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
                'refresh': str(self.refresh),
                'access': str(self.refresh.access_token)
            }
        return response


class ActivateAccountSerializer(CustomValidSerializer):
    """
    Сериализатор для представления активации учетной записи.
    """

    email: str = serializers.CharField(max_length=60, required=True)
    code: str = serializers.CharField(max_length=50, required=True)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        email: str = attrs.get('email')
        code: str = attrs.get('code')

        # Поиск пользователя с этим email
        user: User | None = User.objects.get_object_or_none(email=email)

        # Проверка, есть ли у пользователя такой код
        code_type: int = AccountCode.ACCOUNT_ACTIVATION
        code: AccountCode = user_code_validation(user=user, code=code, code_type=code_type, raise_exception=True)

        # Установка атрибута .user для использования его в .save()
        self.user = user

        # Удаление использованного кода
        code.datetime_expire = timezone.now()
        code.save(update_fields=('datetime_expire',))

        return attrs

    def save(self) -> None:
        """
        Установка значения `is_acitve = True` и сохранение данных.
        """
        self.user.is_active = True

        # Активация учетной записи пользователя
        self.user.save(update_fields=('is_active',))

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': 'Вы успешно подтвердили свою учетную запись.'
        }
        return response


class ChangePasswordSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериалайзер для сброса пароля пользователя.
    """

    old_password: str = serializers.CharField(required=True)
    password: str = serializers.CharField(required=True)
    password2: str = serializers.CharField(required=True)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        old_password: str = attrs.get('old_password')
        password: str = attrs.get('password')
        password2: str = attrs.get('password2')

        # get_user() из AccessTokenMixin и
        # self.request из CommonPostMixin
        user = self.get_user(request=self.request)

        # Устанавливаем атрибут .user, чтобы использовать его затем в .save()
        self.user = user

        # Проверяем, является ли старый пароль допустимым
        old_password_validation_error(user=user, password=old_password, raise_exception=True)

        # Проверяем, является ли новый пароль допустимым
        password_validation_error(password1=password, password2=password2, user=user, raise_exception=True)

        return attrs

    def save(self) -> None:
        """
        Сохранение нового пароля пользователя.
        """
        password: str = self.validated_data.get('password')

        # .user был установлен в .validate()
        user: User = self.user

        # Устанавливаем захешированный пароль пользователю
        user.set_password(password)

        # Устанавливаем захешированный пароль2 пользователю
        user.password2 = user.password

        # Сохраняем данные
        user.save(update_fields=('password', 'password2'))

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': 'Вы успешно сбросили свой пароль.'
        }
        return response


class ForgotPasswordSerializer(CustomValidSerializer):
    """
    Сериалайзер для получения кода сброса пароля пользователя.
    """

    email: str = serializers.CharField(max_length=60, required=True)
    last_name: str = serializers.CharField(min_length=1, required=True)
    first_name: str = serializers.CharField(min_length=1, required=True)
    gender: int = serializers.IntegerField(required=True)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        email: str = attrs.get('email')
        last_name: str = attrs.get('last_name')
        first_name: str = attrs.get('first_name')
        gender: int = attrs.get('gender')

        # Проверяем, является ли электронная почта допустимой
        email_validation_error(email=email, find_user=True, raise_exception=True)

        # Получаем пользователя по электронной почте
        user: User = User.objects.get_object_or_none(email=email)

        # Проверяем валидность данных для сброса пароля
        password_recovery_validation_error(gender=gender, last_name=last_name,
                                           user=user, first_name=first_name,
                                           raise_exception=True)

        # Устанавливаем атрибут .user, чтобы использовать его затем в .save()
        self.user = user

        return attrs

    def save(self) -> None:
        """
        Сохранение данных.
        """
        user: User = self.user

        # AccountCode.PASSWORD_RESET, чтобы код был более читаемым
        code_type: int = AccountCode.PASSWORD_RESET

        # AccountCode.CODE_LENGTH, чтобы код был масштабируемым
        code_length: int = AccountCode.CODE_LENGTH

        # Создаем код сброса пароля новой учетной записи
        AccountCode.objects.create(user=user, code_type=code_type,
                                   code=generate_code(code_length))

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': 'Код сброса пароля был отправлен на вашу электронную почту.'
        }
        return response


class ConfirmPasswordSerializer(CustomValidSerializer):
    """
    Подтвердить код для изменения пароля пользователя.
    """

    code: str = serializers.CharField(max_length=AccountCode.CODE_LENGTH, required=True)
    email: str = serializers.CharField(max_length=60, required=True)
    password: str = serializers.CharField(max_length=128, required=True)
    password2: str = serializers.CharField(max_length=128, required=True)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        password: str = attrs.get('password')
        password2: str = attrs.get('password2')
        email: str = attrs.get('email')
        code: str = attrs.get('code')

        # Проверяем, является ли электронная почта допустимой
        email_validation_error(email=email, find_user=True, raise_exception=True)

        # Проверяем, являются ли пароли допустимыми
        password_validation_error(password1=password, password2=password2, raise_exception=True)

        # Находим пользователя с этой электронной почтой
        user: User = User.objects.get_object_or_none(email=email)

        # Устанавливаем атрибут .user, чтобы использовать его затем в .save()
        self.user = user
        code_type: int = AccountCode.PASSWORD_RESET

        # Проверяем, является ли код допустимым
        code: AccountCode = user_code_validation(user=user, code=code, code_type=code_type, raise_exception=True)
        
        # Удаляем использованный код
        code.datetime_expire: datetime.datetime = timezone.now()
        code.save(update_fields=('datetime_expire',))

        return attrs

    def save(self) -> None:
        """
        Сохранение данных.
        """
        user: User = self.user
        password: str = self.validated_data.get('password')
        user.set_password(password)
        user.password2 = user.password
        user.save(update_fields=('password', 'password2'))

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': 'Вы успешно изменили пароль.'
        }
        return response



class RefreshTokenSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериализатор для обновления токена.
    """

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        # Получаем refresh токен из куков запроса
        token: str = attrs['refresh_token']

        # Проверяем данные refresh токена
        refresh_token_validation_error(token=token, raise_exception=True)

        # Устанавливаем .token, чтобы использовать его затем в .save()
        self.token = token

        return attrs

    def save(self) -> None:
        """
        Сохранение данных.
        """
        # Создаем объект RefreshToken, используя refresh токен
        token: RefreshToken = RefreshToken(token=self.token)

        # Получаем access токен
        self.access_token = token.access_token

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'access': str(self.access_token)
        }
        return response

class LogoutSerializer(CustomValidSerializer, AccessTokenMixin):
    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных выхода из системы.
        """
        # Получаем пользователя из токена
        logged_out_user = self.get_user(request=self.request)

        # Удаляем все токены пользователя
        TokenList.objects.filter(user=logged_out_user).delete()

        # Возвращаем атрибуты, хотя в данном случае они не используются
        return attrs

    def save(self) -> None:
        """
        Сохранение данных. (В данном случае метод не используется, оставлен для совместимости.)
        """
        pass

    def get_response(self) -> dict:
        """
        Возвращение ответа на запрос выхода из системы.
        """
        response: dict = {
            'data': 'Вы успешно вышли из системы.'
        }
        return response


class UserSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериализатор для пользователя.
    """
    first_name: str = serializers.CharField(required=True, max_length=255, label='Имя')
    last_name: str = serializers.CharField(required=True, max_length=255, label='Фамилия')
    email: str = serializers.EmailField(required=True, max_length=160, label='Email')
    gender: str = serializers.CharField(required=True, label='Пол')
    datetime_created: str = serializers.CharField(required=True, label='Время создания')

    def validate_datetime_created(self, value: str) -> str:
        """
        Валидация времени создания пользователя.
        (Здесь можно добавить специфичные проверки, если необходимо)
        """
        return value

    def get_response(self) -> dict:
        """
        Возвращение ответа на запрос пользователя.
        """
        response: dict = {
            'data': 'Данные пользователя успешно получены.'
        }
        return response