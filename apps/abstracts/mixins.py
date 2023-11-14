# Python
from typing import Any

# DRF
from rest_framework.request import Request
from rest_framework.response import Response as JsonResponse
from rest_framework.validators import ValidationError
from django.db.models.query import QuerySet

# Simple JWT
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local
from auths.models import User

class ResponseMixin:
    """Абстрактный вспомогательный класс для респонсов."""

    STATUS_SUCCESS: str = 'Success'
    STATUS_WARNING: str = 'Warning'
    STATUS_ERROR: str = 'Error'
    STATUSES: tuple[str, ...] = (
        STATUS_SUCCESS,
        STATUS_WARNING,
        STATUS_ERROR
    )

    def json_response(
        self,
        data: Any,
        status: str = STATUS_SUCCESS
    ) -> JsonResponse:

        if status not in self.STATUSES:
            raise ValidationError('FATAL ERROR')

        return JsonResponse(
            {
                'status': status,
                'results': data
            }
        )
    
class ObjectMixin:
    """Абстрактный вспомогательный класс для объектов."""

    def get_object(
        self,
        queryset: QuerySet,
        obj_id: str
    ) -> Any:
        """Метод для вытаскивания объекта."""

        obj: Any = queryset.filter(id=obj_id).first()
        if obj is None:
            raise ValidationError(
                {
                    'status': 'Error',
                    'results': f'Object {obj_id} not found'
                }
            )
        return obj
    

class AccessTokenMixin:
    """
    Миксин, который помогает работать с токеном доступа.
    """

    def get_user(self, request: Request) -> tuple[User, dict | None]:
        """
        Используйте только с IsAuthenticated в разрешении_CLASSES.
        """
        # Аутентификация токена
        authenticator: JWTAuthentication = JWTAuthentication()
        user: User = authenticator.get_user(request.auth)

        return user

