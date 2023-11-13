# DRF
from rest_framework import serializers

# Python
from typing import Dict

class CustomValidSerializer(serializers.Serializer):
    """
    Сериализатор для проверки, являются ли переданные поля допустимыми.
    """

    allowed_fields: tuple = ('csrfmiddlewaretoken', '_content_type', '_content')

    def to_internal_value(self, data: Dict) -> Dict:
        """
        Проверка, являются ли переданные данные допустимыми.
        """
        # Допустимые поля
        allowed_fields: set = set(self.get_fields())

        # Ошибки словаря или их возбуждение позже
        error: dict = {}

        # Проверить, все ли переданные поля в допустимых полях
        invalid_fields = set(data.keys()) - allowed_fields - set(self.allowed_fields)

        # Если есть недопустимые поля
        if invalid_fields:
            for field in invalid_fields:
                error[field] = ['Not allowed.']

            raise serializers.ValidationError(error)

        return super().to_internal_value(data)

