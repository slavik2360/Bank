# Django
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

# Python
import datetime
from typing import Any 


class AbstractManager(models.Manager):
    """Абстрактный менеджер для всех моделей"""

    def get_not_deleted(self) -> QuerySet[Any] | None:
        """
        Получить все модели, где время удаления не является ничем.
        """
        queryset: QuerySet[Any] = \
            self.filter(datetime_deleted__isnull=True)

        return queryset

    def get_deleted(self) -> QuerySet[Any] | None:
        """
        Получить все модели, где время удаления не является ничем.
        """
        queryset: QuerySet[Any] = \
            self.filter(datetime_deleted__isnull=False)

        return queryset

    def get_object_or_none(self, **filter: Any) -> Any:
        """
        Получите пользователя или ни чего.
        """
        # Попробуйте получить объект по фильтру
        try:
            obj: Any = self.get(**filter)

        # Set obj to None, if there is no such object
        except Exception as e:
            print(e)
            obj = None

        finally:
            return obj


class AbstractModel(models.Model):
    """Абстрактная модель для всех других моделей."""

    # Время, когда была создана модель
    datetime_created: datetime.datetime = models.DateTimeField(
        verbose_name='время создания',
        default=timezone.now,
        null=True,
        blank=True
    )
    # Время, когда модель была обновлена
    datetime_updated: datetime.datetime = models.DateTimeField(
        verbose_name='время обновления',
        auto_now=True,
        null=True,
        blank=True
    )
    # Время, когда модель была удалена
    datetime_deleted: datetime.datetime = models.DateTimeField(
        verbose_name='время удаления',
        null=True,
        blank=True
    )
    objects: AbstractManager = AbstractManager()

    class Meta:
        abstract: bool = True