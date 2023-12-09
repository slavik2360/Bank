# DRF
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class Permission(BasePermission):

    def has_permission(self, request: Request, view: 'ViewSet') -> bool:
        # Получаем объект пользователя из запроса
        user = request.user

        # Проверяем, если это действие 'destroy'
        if view.action == 'destroy':
            # Разрешаем доступ, если пользователь активен, является сотрудником и суперпользователем
            return user and user.is_active and user.is_staff and user.is_superuser

        # Разрешаем доступ, если пользователь активен
        return user and user.is_active