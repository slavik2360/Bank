# Python
import re
from typing import Union, Literal

# Django
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.conf import settings

# Local
from bank.models import (
    Client,
    Card
)


def card_sender_validation_error(card: str, 
                          raise_exception: bool = False
                         ) -> dict | None:
    """
    Проверяет, существует ли карта в базе данных.

    Возвращает словарь ошибок или None.
    """
    error: dict = {}
    card_exists = Card.objects.filter(number=card).exists()
    
    # Проверка, что введенные данные состоят только из цифр и имеют длину 16 символов
    if not card.isdigit() or len(card) != 16:
        error['card'] = ['Некорректный формат номера карты. Введите 16 цифр.']
    # Проверка, если карты нет возвращаем ошибку 
    if not card_exists:
        error['card'] = ['Некорректный номер карты отправителя.']

    # Если не действителен и функция должна вызывать исключение
    if error and raise_exception is True:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None

def card_receiver_validation_error(card: str, 
                          raise_exception: bool = False
                         ) -> dict | None:
    """
    Проверяет, существует ли карта в базе данных.

    Возвращает словарь ошибок или None.
    """
    error: dict = {}
    card_exists = Card.objects.filter(number=card).exists()
    
    # Проверка, что введенные данные состоят только из цифр и имеют длину 16 символов
    if not card.isdigit() or len(card) != 16:
        error['card'] = ['Некорректный формат номера карты. Введите 16 цифр.']
    # Проверка, если карты нет возвращаем ошибку 
    if not card_exists:
        error['card'] = ['Некорректный номер карты получателя.']

    # Если не действителен и функция должна вызывать исключение
    if error and raise_exception is True:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None

def length_card_validation_error(card_sender: str, 
                                card_receiver: str,
                                raise_exception: bool = False
                                ) -> dict | None:
    """
    Проверяет, существует ли карта в базе данных.

    Возвращает словарь ошибок или None.
    """
    error: dict = {}

    # Проверка, что введенные данные состоят только из цифр и имеют длину 16 символов
    if not (card_sender.isdigit() and card_receiver.isdigit() 
            and len(card_sender) == len(card_receiver) == 16
        ):
        error['card'] = ['Номер карты должен состоять из 16 цифр.']

    # Если не действителен и функция должна вызывать исключение
    if error and raise_exception:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None

def balance_validation_error(user: Client, 
                             amount: float, 
                             raise_exception: bool = False
                            ) -> dict | None:
    """
    Проверяет баланс для выполнения транзакции.

    Возвращает словарь ошибок или None.
    """
    error: dict = {}
    client: Client = Client.objects.get(user=user)

    if client.account_balance < amount:
        error['balance'] = ['Недостаточно средств на балансе для выполнения транзакции.']

    # Если не действителен и функция должна вызывать исключение
    if error and raise_exception:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None

def amount_validation_error(amount: str, 
                            raise_exception: bool = False
                            ) -> dict | None:
    """
    Проверяет сумму для перевода.

    Возвращает словарь ошибок или None.
    """
    error: dict = {}

    try:
        amount = float(amount)
    except ValueError:
        error['amount'] = ['Введите корректное числовое значение.']

    if amount <= 99:
        error['amount'] = ['Минимальная сумма перевода должна быть равно 100₸.']

    # Если не действителен и функция должна вызывать исключение
    if error and raise_exception:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None


def digit_validation_error(amount: str, 
                            raise_exception: bool = False
                            ) -> dict | None:
    """
    Проверяет сумму для пополнения счета.

    Возвращает словарь ошибок или None.
    """
    error: dict = {}

    try:
        amount = float(amount)
    except ValueError:
        error['amount'] = ['Введите корректное числовое значение.']

    if amount <= 99:
        error['amount'] = ['Минимальная сумма должна быть равна 100₸.']

    # Если не действителен и функция должна вызывать исключение
    if error and raise_exception:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None