# Python
from typing import Any

# Django
from auths.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **kwargs: Any) -> None:
        try:
            User.objects.create_superuser(
                email='root@root.com',
                first_name='root',
                last_name='admin',
                password='qazwsx22'
            )
            print('Админ успешно создан')
            User.objects.create_user(
                email='slv@slv.com',
                first_name='slv',
                last_name='user',
                password='qazwsx22',
                password2='qazwsx22',
                gender=1
            )
            print('Пользователь успешно создан')
        except Exception as exc:
            print(f'Админ не создан: {str(exc)}')