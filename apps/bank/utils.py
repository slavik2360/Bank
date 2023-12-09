# Python
from typing import Any, Optional

# local
from bank.models import Card, Transaction


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