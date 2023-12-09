# Python
import logging
import datetime

# django
from django.db import models
from django.db.models.query import QuerySet
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator
)

#Local
from auths.models import User
from abstracts.models import (
    AbstractModel,
    AbstractManager,
)

logger = logging.getLogger(__name__)

class ClientManager(AbstractManager):
    """
    Менеджер модели клиента.
    """
    def get_clients_with_balance_over(self, amount: float) -> QuerySet['Client']:
        """
        Возвращает клиентов с балансом выше указанной суммы.

        :param amount: Минимальная сумма баланса.
        :return: QuerySet с клиентами, у которых баланс выше указанной суммы.
        """
        return self.filter(account_balance__gt=amount)


class Client(AbstractModel):
    """
    Модель клиента банка. 
    """
    user: 'User' = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance: float = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        validators=[
            MinValueValidator(
                0, 
                message='Баланс не может быть ниже нуля.'
            )
        ]
    )

    objects = ClientManager()

    def __str__(self):
        return self.user.fullname
    
    class Meta:
        ordering = (
            'datetime_created',
        )
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class CardManager(AbstractManager):
    """
    Менеджер модели карты.
    """
    def create_card(self, card_number: str, cvv: str) -> 'Card':
        """
        Создает и сохраняет карту по номеру, CVV и сроку годности.
        """
        new_card = self.model(
            number=card_number,
            cvv=cvv
        )
        new_card.save()
        return new_card
    
    def get_active_cards_for_client(self, client: 'Client') -> QuerySet['Card']:
        """
        Возвращает активные карты для указанного клиента.

        :param client: Клиент, для которого необходимо получить активные карты.
        :return: QuerySet активных карт.
        """
        return self.filter(client=client, is_active=True)

    def get_card_by_number(self, card_number: str) -> 'Card':
        """
        Возвращает карту по её номеру.

        :param card_number: Номер карты.
        :return: Экземпляр карты.
        """
        return self.get(card_number=card_number)

    def deactivate_card(self, card_number: str) -> None:
        """
        Деактивирует карту с указанным номером.

        :param card_number: Номер карты.
        """
        card = self.get_card_by_number(card_number)
        card.is_active = False
        card.save()
        logger.info(f"Карта {card_number} была деактивирована.")

    def block_card(self, card_number: str) -> None:
        """
        Блокирует карту с указанным номером.

        :param card_number: Номер карты.
        """
        card = self.get_card_by_number(card_number)
        card.is_active = False
        card.save()
        logger.info(f"Карта {card_number} была заблокирована.")


class Card(AbstractModel):
    """
    Модель карты.
    """
    # Ограничение выпускаемых карт
    LIMIT_CARD: int = 1
    ONE_YEAR = 365

    # Владелец карты
    client: Client = models.ForeignKey(
        verbose_name='владелец',
        to=Client,
        on_delete=models.PROTECT,
        related_name='cards',
        null=True,
        blank=True
    )
    # Номер банковской карты
    number: str = models.CharField(
        verbose_name='номер карты',
        max_length=16,
        validators=(
            MinLengthValidator(16),
        ),
        unique=True
    )
    # CVV код карты
    cvv: str = models.CharField(
        verbose_name='cvv',
        max_length=3,
        validators=(
            MinLengthValidator(3),
        )
    )
    # Cрок годности карты карты
    date_expiration = models.DateField(
        verbose_name='дата истечения',
        default=datetime.datetime.today() + datetime.timedelta(
            days=ONE_YEAR
        )
    )
    is_active = models.BooleanField(
        default=True
    )
    # Менеджер
    objects: CardManager = CardManager()

    def __str__(self) -> str:
        return f"{self.client}->{self.number}"

    class Meta:
        ordering = (
            'client__user__id', 
            'datetime_created'
        )
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'


class TransactionManager(AbstractManager):
    """
    Менеджер модели транзакции.
    """
    def get_transactions_for_user(self, client: 'Client') -> 'QuerySet[Transaction]':
        """
        Возвращает транзакции для указанного клиента.

        :param client: Клиент, для которого нужно получить транзакции.
        :return: QuerySet с транзакциями, в которых клиент является отправителем или получателем.
        """
        return self.filter(models.Q(sender=client) | models.Q(receiver=client))


class Transaction(AbstractModel):
    """
    Модель транзакции.
    """
    sender: Card = models.ForeignKey(
        verbose_name='отправитель',
        to=Card,
        on_delete=models.PROTECT,
        related_name='transactions_sended',
        blank=True,
        null=True
    )
    # Получатель карт денег
    receiver: Card = models.ForeignKey(
        verbose_name='получатель',
        to=Card,
        on_delete=models.PROTECT,
        related_name='transactions_received',
        blank=True,
        null=True
    )
    # Cумма перевода
    amount: float = models.DecimalField(
        verbose_name='сумма перевода',
        max_digits=10,
        decimal_places=2
    )
    # Менеджер
    objects: TransactionManager = TransactionManager()

    def __str__(self) -> str:
        return f"{self.sender.number} -> {self.receiver.number}"

    class Meta:
        ordering = (
            'id',
        )
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'