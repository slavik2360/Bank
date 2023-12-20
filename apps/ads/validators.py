# Django
from django.core.exceptions import ValidationError

# Local
from bank.models import Client



def balance_validation_error(user: Client, 
                             amount: float, 
                             raise_exception: bool = False
                            ) -> dict | None:
    """
    Проверяет баланс для создания объявления.

    Возвращает словарь ошибок или None.
    """
    error: dict = {}
    client: Client = Client.objects.get(user=user)

    if client.account_balance < amount:
        error['balance'] = ['Недостаточно средств на балансе.']

    # Если не действителен и функция должна вызывать исключение
    if error and raise_exception:
        raise ValidationError(error)

    # Вернуть ошибки или None
    return error if error else None