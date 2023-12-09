# Django
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.conf import settings
import jwt

# Python
from datetime import datetime, timedelta
from typing import Any

# Local
from abstracts.models import (
    AbstractModel,
    AbstractManager,
)
 


class UserManager(BaseUserManager, AbstractManager):
    """
    Менеджер для пользовательских методов создания пользовательской модели.
    """

    def create_user(self, email: str, first_name: str,
                    last_name: str, password: str,
                    password2: str) -> 'User':
        """
        Создает и возвращает пользователя с имейлом, паролем и именем.
        """

        if email is None:
            raise TypeError('У пользователи должен быть адрес электронной почты.')
        
        user: 'User' = self.model(email=self.normalize_email(email), first_name=first_name,
                       last_name=last_name, password=password,
                       password2=password2)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, first_name: str,
                         last_name: str, password: str) -> 'User':
        """
        Создает и возввращет пользователя с привилегиями суперадмина.
        """
        if password is None:
            raise TypeError('Администратор должен иметь пароль.')
        
        user: 'User' = self.model(email=self.normalize_email(email), first_name=first_name,
                       last_name=last_name, password=password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_user_or_none(self, **filter: Any) -> 'User':
        """
        Получить пользователя или None по фильтру.
        """
        try:
            user: 'User' = self.get(**filter)
        except User.DoesNotExist:
            user = None
        return user


class User(PermissionsMixin, AbstractBaseUser, AbstractModel):
    """
    Кастомная модель пользователя.
    """
    # Имя пользователя
    first_name: str = models.CharField(
        verbose_name='имя',
        max_length=40
    )
    # Фамилия пользователя
    last_name: str = models.CharField(
        verbose_name='фамилия',
        max_length=40
    )
    # Электронная почта/логин пользователя,регистрации и входе в систему
    email: str = models.CharField(
        verbose_name='почта/логин',
        max_length=60,
        unique=True
    )
    # Пароль1 Хэшировать в signals.py при создании!
    password: str = models.CharField(
        verbose_name='пароль1',
        max_length=128,
        validators=(
            MinLengthValidator(7),
        )
    )
    # Пароль2, чтобы убедиться, что если пользователь ввел правильный пароль
    password2: str = models.CharField(
        verbose_name='пароль2',
        max_length=128,
        validators=(
            MinLengthValidator(7),
        )
    )
    # Есть ли учетная запись пользователя подтверждена для ее использования
    is_active: bool = models.BooleanField(
        verbose_name='активный?',
        default=False
    )
    # Есть ли у пользователя есть привилегия администратора
    is_staff: bool = models.BooleanField(
        verbose_name='это персонал',
        default=False
    )
    is_superuser: bool = models.BooleanField(
        verbose_name='Суперпользователь',
        default=False
    )
    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: tuple = (
        'first_name',
        'last_name',
        'password'
    )
    # Пользовательский диспетчер
    objects: UserManager = UserManager()

    # Получить фамилию пользователя + Имя
    @property
    def fullname(self) -> str:
        return '%s %s' % (self.last_name, self.first_name)

    # Проверка, есть ли у пользователя привилегии администратора
    @property
    def is_admin(self) -> bool:
        """
        Используется для аутентификации суперпользователя.
        """
        return self.is_active and self.is_superuser and self.is_staff
    
    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token().
        """
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
        'id': self.pk,
        'exp': int(dt.strftime('%s')),
        'is_active': self.is_active 
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def __str__(self) -> str:
        return self.fullname

    class Meta:
        ordering = (
            'datetime_created',
        )
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class CodeManager(models.Manager):
    """
    Менеджер для управления кодами.
    """

    def extended_filter(self, expired: bool, **kwargs: dict) -> 'AccountCode':
        """
        Расширенный фильтр для управления кодами.

        :param expired: Флаг, указывающий, следует ли проверять срок действия кода.
        :param kwargs: Дополнительные параметры для фильтрации кодов.
        :return: QuerySet кодов, соответствующих заданным критериям.
        """
        now = timezone.now()
        filter_params = {'datetime_expire__lt': now} if expired else {'datetime_expire__gt': now}
        queryset = self.filter(**kwargs, **filter_params)
        return queryset

class AccountCode(models.Model):
    """
    Код для пользователей для подтверждения различных действий.
    """
    # Длина активационного кода
    CODE_LENGTH: int = 4
    # Время жизни кода
    LIFETIME: timezone.timedelta = timezone.timedelta(minutes=10)
    # Код активации аккаунта
    ACCOUNT_ACTIVATION: int = 1
    # Код сброса пароля
    PASSWORD_RESET: int = 2
    TYPES: tuple = (
        (ACCOUNT_ACTIVATION, 'ACCOUNT-ACTIVATION'),
        (PASSWORD_RESET, 'PASSWORD-RESET'),
    )
    code_type: int = models.PositiveSmallIntegerField(
        verbose_name='тип кода',
        choices=TYPES,
        default=ACCOUNT_ACTIVATION
    )
    user: 'User' = models.ForeignKey(
        verbose_name='пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='activate_account_codes',
        null=True
    )
    code: str = models.CharField(
        verbose_name='код',
        max_length=CODE_LENGTH,
        validators=(
            MinLengthValidator(CODE_LENGTH),
        )
    )
    # Время когда код, когда код считается истекшим
    datetime_expire: timezone.datetime = models.DateTimeField(
        verbose_name='время окончания действия кода'
    )

    objects: CodeManager = CodeManager()

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения объекта.
        Устанавливает время окончания действия кода при создании.
        """
        if not self.pk:
            self.datetime_expire = timezone.now() + self.LIFETIME
        super().save(*args, **kwargs)

    class Meta:
        ordering = (
            'datetime_expire',
        )
        verbose_name = 'код активации'
        verbose_name_plural = 'коды активации'


class TokenManager(AbstractManager):
    """
    Менеджер для refresh-токенов.
    """

    def find_valid(self, token: str, user: User = None) -> 'TokenList':
        """
        Находит все действительные токены.
        """
        # Получаем текущее время
        current_time = timezone.now()

        # Проверяем, не истек ли токен
        queryset: QuerySet[TokenList] = \
            TokenList.objects.filter(expire_datetime__gt=current_time)

        # Если нужно найти активный refresh-токен для пользователя
        if user:
            queryset = queryset.filter(user=user, refresh_token=token)

        return queryset


class TokenList(AbstractModel):
    """
    Модель для refresh-токенов.
    """

    user: User = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='refresh_tokens',
        null=True,
        help_text='Связанный пользователь'
    )
    refresh_token: str = models.CharField(
        verbose_name='Токен',
        max_length=300,
        null=True
    )
    # Время, когда срок действия токена истек
    expire_datetime: timezone.datetime = models.DateTimeField(
        verbose_name='Время истечения токена'
    )
    # Менеджер
    objects: TokenManager = TokenManager()

    class Meta:
        ordering = (
            'expire_datetime',
        )
        verbose_name = 'список токена'
        verbose_name_plural = 'список токенов'
