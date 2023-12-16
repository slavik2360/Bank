# DRF 
from rest_framework import serializers
from django.core.exceptions import ValidationError

# Local
from abstracts.mixins import AccessTokenMixin
from abstracts.serializers import CustomValidSerializer
from auths.models import User
from bank.models import Client
from ads.models import (
    Ads,
    AdHistory
)
from bank.validators import (
    digit_validation_error,
    balance_validation_error
)


class AdsCreateSerializer(CustomValidSerializer, AccessTokenMixin):

    title = serializers.CharField(max_length=120)
    description = serializers.CharField(max_length=120)
    price = serializers.DecimalField(decimal_places=2, max_digits=10)
    image = serializers.ImageField(required=False)

    def validate(self, attrs: dict) -> dict:
        """
        Валидация данных.
        """
        price = attrs.get('price')
        request = self.context.get('request')
        user = self.get_user(request=request)

        # Проверка, что сумма соответсвует параметрам
        digit_validation_error(amount=price, raise_exception=True)

        # Проверка, средств на балансе
        balance_validation_error(user=user, amount=price, raise_exception=True)

        # Установка атрибута .user для использования его в .save()
        self.user = user
        return attrs

    def save(self) -> None:
        """
        Сохранение нового объявления.
        """
        title = self.validated_data['title']
        description = self.validated_data['description']
        price = self.validated_data['price']
        image = self.validated_data.get('image')

        # Получаем клиента
        client: Client = Client.objects.get(user=self.user)

        if image:
            Ads.objects.create(title=title, customer=client, description=description, price=price, image=image)
        else:
            Ads.objects.create(title=title, customer=client, description=description, price=price)

    def get_response(self) -> dict:
        """
        Возврат ответа представлению.
        """
        response = {
            'data': 'Вы успешно создали объявление.'
        }
        return response
    
    
class AdsTakeJobSerializer(CustomValidSerializer, AccessTokenMixin):
    def validate(self, attrs):
        """
        Валидация данных.
        """

        return attrs

    def save(self, ad: Ads, acting_client: Client) -> None:
        """
        Метод для взятия работы исполнителем.

        :param ad: Объект объявления.
        :type ad: Ads
        :param acting_client: Объект исполнителя.
        :type acting_client: Client
        :raises serializers.ValidationError: Если не удалось взять работу.
        """
        try:
            ad.take_job(acting_client)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

    def get_response(self):
        """
        Возврат ответа представлению.
        """
        response = {
            'data': 'Работа успешно взята.'
        }
        return response
    

class AdsCompleteJobSerializer(CustomValidSerializer, AccessTokenMixin):
    def validate(self, attrs):
        """
        Валидация данных.
        """
        return attrs

    def save(self, ad: Ads, acting_client: Client):
        """
        Метод для завершения выполнения заказа.

        :param ad: Объект объявления.
        :type ad: Ads
        :param acting_client: Объект исполнителя.
        :type acting_client: Client
        :raises serializers.ValidationError: Если не удалось завершить выполнение заказа.
        """
        try:
            ad.complete_job()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    def get_response(self):
        """
        Возврат ответа представлению.
        """
        response = {
            'data': 'Работа успешно выполнена.'
        }
        return response
    

class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'


class AdHistorySerializer(serializers.ModelSerializer):
    datetime_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = AdHistory
        fields = '__all__'