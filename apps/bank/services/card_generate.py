# Python
import random

# DRF
from auths.models import User
from bank.models import Client

# Local
from bank.models import Card
from django.db import IntegrityError

class GenerateCard:
    """
    Клас для создания виртуальной карты.
    
    :param card_number: 51694971********.

    :return: Экземпляр карты.
    """

    def __init__(self, client: Client) -> 'Client':
        self.client = client

    def generate_number(self) -> str:
        """
        Создать уникальный номер для карты.
        """
        # Создаем код карты
        number = f'51694971{self.client.cards.count() + 1}{"".join(random.choices("0123456789", k=7))}'

        return number

    def generate_cvv(self) -> str:
        """
        Создать cvv для карты.
        """
        # Создаем cvv код
        cvv = random.randrange(100, 1000)

        return str(cvv)

    def generate(self) -> Card:
        """
        Создайте новую карту и заполните данные.
        """
        while True:
            try:
                new_card, created = Card.objects.get_or_create(
                    number=self.generate_number(),
                    defaults={
                        'cvv': self.generate_cvv(),
                        'client': self.client,
                        'is_active': True,
                    }
                )
                if created:
                    return new_card
            except IntegrityError:
                continue