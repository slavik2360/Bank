# django
from django.db import models
from django.db.models import F
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.core.validators import (
    MinValueValidator,
    FileExtensionValidator
)

#Local
from bank.models import Client
from abstracts.models import (
    AbstractModel,
    AbstractManager,
)

class Ads(AbstractModel):
    """
    Модель объявления.
    """

    def default_poster() -> str:
        return '/ads_default/ads.png'
    
    STATUS_ACTIVE = 0
    STATUS_PROGRESS = 1
    STATUS_COMPLETED = 2
    STATUSS = (
        (STATUS_ACTIVE, 'Активен'),
        (STATUS_PROGRESS, 'Выполняется'),
        (STATUS_COMPLETED, 'Выполнен')
    )

    title: str = models.CharField(
        verbose_name='наименование',
        max_length=120
    )
    description: str = models.CharField(
        verbose_name='описание',
        max_length=120
    )
    status: int = models.PositiveSmallIntegerField(
        choices=STATUSS,
        verbose_name='статус',
        default=STATUS_ACTIVE
    )
    image: str = models.ImageField(
        verbose_name='изображение',
        upload_to='adsImage',
        validators=[FileExtensionValidator(
            allowed_extensions=[
                'png', 'jpg', 'jpeg',
            ],
            message='Извините, этот формат файла не поддерживается'
        )],
        default=default_poster,
        blank=True,
        null=True
    )
    customer: Client = models.ForeignKey(
        verbose_name='заказчик',
        to=Client,
        on_delete=models.CASCADE,
        related_name='customer_ads',
        blank=True,
        null=True
    )
    acting: Client = models.ForeignKey(
        verbose_name='исполнитель',
        to=Client,
        on_delete=models.CASCADE,
        related_name='acting_ads',
        blank=True,
        null=True
    )
    price: float = models.DecimalField(
        verbose_name='цена',
        decimal_places=2,
        max_digits=10
    )

    def take_job(self, acting_client):
        """
        Метод для взятия работы исполнителем.

        :param acting_client: Объект исполнителя.
        :raises ValidationError: Если статус объявления не активен.
        """
        if self.status != self.STATUS_ACTIVE:
            raise ValidationError("Нельзя взять работу с текущим статусом объявления.")

        self.status = self.STATUS_PROGRESS
        self.acting = acting_client
        self.save()

    def complete_job(self):
        """
        Метод для завершения работы и списания денег.

        :raises ValidationError: Если статус объявления не в процессе выполнения.
        :raises ValidationError: Если у заказчика недостаточно средств для оплаты.
        """

        if self.status != self.STATUS_PROGRESS:
            raise ValidationError("Нельзя завершить работу с текущим статусом объявления.")

        with transaction.atomic():
            ad = Ads.objects.select_for_update().get(pk=self.pk)

            if ad.customer and ad.acting:
                if ad.customer.account_balance >= ad.price:
                    ad.status = self.STATUS_COMPLETED
                    ad.save()

                    # Сохраняем историю транзакции
                    AdHistory.objects.create(
                        client=ad.customer,
                        ads=ad,
                        amount=ad.price,
                        transaction_type='debit'
                    )
                    AdHistory.objects.create(
                        client=ad.acting,
                        ads=ad,
                        amount=ad.price,
                        transaction_type='credit'
                    )

                    # Списываем деньги у заказчика и зачисляем исполнителю
                    ad.customer.account_balance -= ad.price
                    ad.acting.account_balance += ad.price

                    ad.customer.save()
                    ad.acting.save()
                else:
                    raise ValidationError("Недостаточно средств у заказчика для оплаты.")

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'

    def __str__(self) -> str:
        return f'{self.customer} <:> {self.acting} - price {self.price}'
    

class AdHistory(AbstractModel):
    """
    Модель истории объявлений.
    """
    TRANSACTION_TYPES = (
        ('debit', 'Списание'),
        ('credit', 'Зачисление'),
    )
    client: Client = models.ForeignKey(
        verbose_name='чье объявление?',
        to=Client,
        on_delete=models.CASCADE,
        related_name='history',
        blank=True,
        null=True
    )
    ads: Ads = models.ForeignKey(
        verbose_name='объявление',
        to=Ads,
        on_delete = models.CASCADE,
        related_name='history'
    )
    amount: float = models.DecimalField(
        verbose_name='стоимость',
        decimal_places=2,
        max_digits=10
    )
    transaction_type: str = models.CharField(
        verbose_name='тип транзакции',
        choices=TRANSACTION_TYPES,
        max_length=10
    )

    class Meta:
        ordering = (
            'id', 
        )
        verbose_name = 'История объявлений'
        verbose_name_plural = 'Истории объявлений'

    def __str__(self) -> str:
        return f'{self.client} <:> {self.transaction_type} - price {self.amount}'