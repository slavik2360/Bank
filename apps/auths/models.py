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

# Python
import datetime
from typing import Any

# Третья сторона
from abstracts.models import (
    AbstractModel,
    AbstractManager,
)


class UserManager(BaseUserManager, AbstractManager):
    """
    Manager for custom create methods for user model.
    """

    def create_superuser(self, email: str, first_name: str,
                         last_name: str, password: str) -> 'User':
        """
        Create super user method.
        """
        u: User = User(email=email, first_name=first_name,
                       last_name=last_name, password=password)
        u.is_superuser = True
        u.is_active = True
        u.is_staff = True
        u.save(using=self._db)
        return u

    def create_user(self, email: str, first_name: str,
                    last_name: str, password: str,
                    password2: str) -> 'User':
        """
        Create default user method.
        """
        u: User = User(email=email, first_name=first_name,
                       last_name=last_name, password=password,
                       password2=password2)
        u.save(using=self._db)
        return u

    def get_user_or_none(self, **filter: Any) -> 'User':
        """
        Get user or None by field.
        """
        try:
            user: User = self.get(**filter)
        except User.DoesNotExist:
            user = None
        finally:
            return user


class User(PermissionsMixin, AbstractBaseUser, AbstractModel):
    """
    Custom model of user.
    """
    class Geders(models.TextChoices):
        MALE= 'MALE', 'Мужчина'
        FEMALE = 'FEMALE', 'Женщина'
    # Все возможные пол пользователя
    # MALE: int = 1
    # FEMALE: int = 2
    # GENDERS: tuple = (
    #     (MALE, 'male'),
    #     (FEMALE, 'female'),
    # )
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
    # Пол пользователя
    gender: int = models.SmallIntegerField(
        verbose_name='gender',
        choices=Geders,
        null=True
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

    # Проверьте, есть ли у пользователя привилегии администратора
    @property
    def is_admin(self) -> bool:
        """
        Used for superuser authentication.
        """
        return self.is_active and self.is_superuser and self.is_staff

    def __repr__(self) -> str:
        return self.fullname

    class Meta:
        ordering = (
            'datetime_created',
        )
        verbose_name = 'user'
        verbose_name_plural = 'users'