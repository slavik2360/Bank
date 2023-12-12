# Python
import logging
import random
import decouple

# DRF
from rest_framework import serializers

# Local
from auths.models import User
from abstracts.mixins import AccessTokenMixin
from abstracts.serializers import CustomValidSerializer
from bank.services.card_generate import GenerateCard
from bank.services.currency_request import crate_exchange_currency
from bank.models import (
    Client,
    Card,
    Transaction,
    ExchangeRate
)
from bank.validators import (
    card_validation_error,
    length_card_validation_error,
    amount_validation_error,
    balance_validation_error,
    digit_validation_error
)

logger = logging.getLogger(__name__)

class CreateClientAndCardSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериалайзер для создания клиента и карты.
    """
    def create_client_and_card(self, user: User) -> None:
        # Создание клиента, если его еще нет
        client, _ = Client.objects.get_or_create(user=user)

        # Проверка, если карта уже выпущена
        if client.cards.count() >= Card.LIMIT_CARD:
            raise serializers.ValidationError({'card': ['Вы можете выпустить только одну карту.']})

        # Создание экземпляра генератора карты и генерация новой карты
        generator = GenerateCard(client=client)
        card = generator.generate()

        self.card = card
        
    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': f'Карта {self.card.number} успешно создана.'
        }
        return response


class RequisiteSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериалайзер для вывода данных о карте.
    """
    account_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    card_number = serializers.CharField(source='cards.first.number', read_only=True)
    card_cvv = serializers.CharField(source='cards.first.cvv', read_only=True)
    card_expiry_date = serializers.DateField(source='cards.first.date_expiration', read_only=True)

    def get_full_name(self, client: Client) -> str:
        return f"{client.user.fullname}"

    def to_representation(self, instance: Client) -> dict:
        data = super().to_representation(instance)
        data['full_name'] = self.get_full_name(instance)
        return data


class FillBalanceSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериалайзер для пополнения средств.
    """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        amount_transacrion: str = attrs.get('amount')

        # Проверка, что сумма перевода соответсвует параметрам
        digit_validation_error(amount=amount_transacrion, raise_exception=True)
        
        return attrs

    def save(self) -> None:
        """
        Сохранение данных.
        """
        amount = self.validated_data['amount']
        request = self.context.get('request')
        user = self.get_user(request=request)

        # Получаем клиента
        client: Client = Client.objects.get(user=user)

        # Увеличиваем баланс 
        client.account_balance += amount
        client.save()

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': 'Транзакция успешно выполнена.'
        }
        return response


class RefillTransactionSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериалайзер для перевода средств.
    """
    sender = serializers.CharField(max_length=16, required=True)
    receiver = serializers.CharField(max_length=16, required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        sender_card_number: str = attrs.get('sender')
        receiver_card_number: str = attrs.get('receiver')
        amount_transacrion: str = attrs.get('amount')

        # Проверка, что карта существует в базе данных
        card_validation_error(card=receiver_card_number, raise_exception=True)
        # Проверка, что номер карты соответствует длине
        length_card_validation_error(card_sender=sender_card_number, 
                                     card_receiver=receiver_card_number,
                                     raise_exception=True
                                    )
        # Проверка, что сумма перевода соответсвует параметрам
        amount_validation_error(amount=amount_transacrion, raise_exception=True)
        
        return attrs

    def save(self) -> None:
        """
        Сохранение данных.
        """
        sender_card_number = self.validated_data['sender']
        receiver_card_number = self.validated_data['receiver']
        amount = self.validated_data['amount']

        # Проверяем существование карты получателя
        try:
            sender_card = Card.objects.get(number=sender_card_number)
        except Card.DoesNotExist:
            # Если карта отправителя не существует, создаем ее
            sender_cvv = random.randrange(100, 1000)
            Card.objects.create_card(card_number=sender_card_number, cvv=sender_cvv)
            sender_card = Card.objects.get(number=sender_card_number)

        # Получаем карту получателя
        receiver_card = Card.objects.get(number=receiver_card_number)
        receiver_client: Client = receiver_card.client

        # Увеличиваем баланс получателя
        receiver_client.account_balance += amount
        receiver_client.save()

        # Создаем объект Transaction
        transaction: Transaction = Transaction(
            sender=sender_card,
            receiver=receiver_card,
            amount=amount
        )
        transaction.save()

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': 'Транзакция успешно выполнена.'
        }
        return response


class TransferTransactionSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериалайзер для перевода средств.
    """
    sender = serializers.CharField(max_length=16, required=True)
    receiver = serializers.CharField(max_length=16, required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        sender_card_number: str = attrs.get('sender')
        receiver_card_number: str = attrs.get('receiver')
        amount_transacrion: str = attrs.get('amount')
        request = self.context.get('request')
        client = self.get_user(request=request)

        # Проверка, что карта существует в базе данных
        card_validation_error(card=sender_card_number, raise_exception=True)
        # Проверка, что номер карты соответствует длине
        length_card_validation_error(card_sender=sender_card_number, 
                                     card_receiver=receiver_card_number,
                                     raise_exception=True
                                    )
        # Проверка, что сумма перевода соответсвует параметрам
        amount_validation_error(amount=amount_transacrion, raise_exception=True)
        # Проверка, средств на балансе
        balance_validation_error(user=client,
                                 amount=amount_transacrion,  
                                 raise_exception=True
                                )
        return attrs

    def save(self) -> None:
        """
        Сохранение данных.
        """
        sender_card_number = self.validated_data['sender']
        receiver_card_number = self.validated_data['receiver']
        amount = self.validated_data['amount']

        # Проверка существования карты отправителя
        try:
            receiver_card = Card.objects.get(number=receiver_card_number)
        except Card.DoesNotExist:
            # Если карта отправителя не существует, создаем ее
            receiver_cvv = random.randrange(100, 1000)
            Card.objects.create_card(card_number=receiver_card_number , cvv=receiver_cvv)
            receiver_card = Card.objects.get(number=receiver_card_number )

        # Получаем карту получателя
        sender_card = Card.objects.get(number=sender_card_number)
        sender_client: Client = sender_card.client

        # Увеличиваем баланс получателя
        sender_client.account_balance -= amount
        sender_client.save()

        # Создаем объект Transaction
        transaction: Transaction = Transaction(
            sender=sender_card,
            receiver=receiver_card,
            amount=amount
        )
        transaction.save()

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': 'Транзакция успешно выполнена.'
        }
        return response


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['number', 'client']

class TransactionSerializer(CustomValidSerializer, AccessTokenMixin):
    """
    Сериалайзер для истории переводов.
    """
    sender = serializers.CharField(source='sender.client.user', read_only=True)
    sender_card = CardSerializer(source='sender', read_only=True)
    receiver = serializers.CharField(source='receiver.client.user', read_only=True)
    receiver_card = CardSerializer(source='receiver', read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    datetime_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        fields = ['sender', 'sender_card', 'receiver', 'receiver_card', 'amount', 'datetime_created']


class CreateCurrencySerializer(CustomValidSerializer):
    """
    Сериалайзер для создания актуальной валюты KZT to ... .
    """
    def create_currecy(self) -> None:
        api_key = decouple.config('CURRENCY_KEY', cast=str)
        base_currency = 'KZT'
        # список конвертируемой валюты
        target_currencies = ['USD', 'EUR', 'RUB', 'GBP', 'JPY', 'CNY']

        crate_exchange_currency(api_key=api_key,
                                base_currency=base_currency,
                                target_currencies=target_currencies
                                )

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response: dict = {
            'data': f'Валюта успешно обновленна.'
        }
        return response
    

class ExchangeRateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для получения актуальной валюты KZT to ... .
    """
    class Meta:
        model = ExchangeRate
        fields = '__all__'