# Python
from typing import Any, Optional
# local
from bank.models import Card, Transaction


def create_transaction(**kwargs: Any) -> Transaction:
    """
    Создает объект транзакции.

    :param kwargs: number1 (отправитель), number2(получатель), сумму.
    """
    # Определение карты отправителя
    card_sender: str = kwargs.get('number1')
    sender: Optional[Card] = None
    if card_sender is not None:
        sender = Card.objects.get(number=card_sender)

    # Определение карты получателя
    card_receiver: str = kwargs.get('number2')
    receiver: Optional[Card] = None
    if card_receiver is not None:
        receiver = Card.objects.get(number=card_receiver)

    # Определение других полей
    balance: float = kwargs.get('balance')

    # Создание транзакции
    transaction: Transaction =\
        Transaction.objects.create(card_receiver=receiver, 
                                   balance=balance,
                                   card_sender=sender)

    return transaction


def calculate_exchange_rate(base_currency_amount: float, target_currency_amount: float) -> float:
    """
    Рассчитывает обменный курс между двумя валютами.

    :param base_currency_amount: Сумма в базовой валюте
    :param target_currency_amount: Эквивалентная сумма в целевой валюте
    :return: Обменный курс
    """
    if base_currency_amount == 0:
        raise ValueError("Сумма базовой валюты должна быть больше нуля")

    exchange_rate = target_currency_amount / base_currency_amount
    return exchange_rate


def convert_to_foreign_currency(amount_in_tenge, exchange_rate):
    """
    Конвертирует сумму из тенге в другую валюту.

    :param amount_in_tenge: Сумма в тенге для конвертации.
    :param exchange_rate: Обменный курс (сколько тенге за одну единицу иностранной валюты).
    :return: Сумма в иностранной валюте.
    """
    foreign_amount = amount_in_tenge / exchange_rate
    
    return foreign_amount