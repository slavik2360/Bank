# Python
from typing import Any
# DRF
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response as JsonResponse


class CommonPostView(GenericAPIView):
    """
    Представление для обработки метода POST с общей логикой.
    """

    permission_classes: tuple = (AllowAny,)
    serializer_class: Any = ...
    success_status: int = 200

    def post(self, request: Request) -> JsonResponse:
        """
        Запрос POST.
        """
        # Десериализация данных
        serializer = self.serializer_class(data=request.data)

        # Установка атрибута .request в сериализаторе. Нам это понадобится затем
        serializer.request = request

        # Валидация данных с возбуждением исключения
        serializer.is_valid(raise_exception=True)

        # Сохранение данных
        serializer.save()

        # Получение ответа от сериализатора (пользовательский метод)
        response = serializer.get_response()

        # Возвращение ответа
        return JsonResponse(data=response, status=self.success_status)

