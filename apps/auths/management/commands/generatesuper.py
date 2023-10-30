# Python
from typing import Any

# Django
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **kwargs: Any) -> None:
        try:
            User.objects.create_superuser(
                username='root',
                email='root@root.com',
                password='qwe',
                first_name='Вячеслав',
                last_name='Администратор'
            )
            print('Админ успешно создан')
        except Exception as exc:
            print(f'Админ не создан: {str(exc)}')