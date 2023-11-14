# Django
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Python
import datetime
from typing import Any 


class AbstractManager(models.Manager):
    """Абстрактный менеджер для всех моделей"""

    def get_not_deleted(self) -> QuerySet[Any]:
        """
        Получить QuerySet всех объектов модели, 
        где время удаления не установлено.
        """
        return self.filter(datetime_deleted__isnull=True)

    def get_deleted(self) -> QuerySet[Any]:
        """
        Получить QuerySet всех объектов модели, 
        где время удаления установлено
        """
        return self.filter(datetime_deleted__isnull=False)

    def get_object_or_none(self, **filter: Any) -> Any | None:
        """
        Получить объект модели по заданным параметрам или None, 
        если объект не существует.
        """
        try:
            obj: Any = self.get(**filter)
        except ObjectDoesNotExist:
            obj = None

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