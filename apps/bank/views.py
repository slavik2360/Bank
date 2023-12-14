# Python
from typing import Optional, Any

# DRF
from rest_framework.request import Request
from rest_framework.response import Response as JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404

# Local
from bank.paginators import TransactionPageNumberPaginator
from abstracts.mixins import (
    AccessTokenMixin,
    ObjectMixin
)
from bank.models import (
    Client,
    Card,
    Transaction,
    ExchangeRate
)
from bank.serializers import (
    CreateClientAndCardSerializer,
    RequisiteSerializer,
    RefillTransactionSerializer,
    TransferTransactionSerializer,
    TransactionSerializer,
    CreateCurrencySerializer,
    ExchangeRateSerializer,
    FillBalanceSerializer
)

class BankViewSet(AccessTokenMixin, ObjectMixin, ViewSet):
    """
    Представление для моделей Банка.
    """
    """
    API api/v1/bank/...
    """

    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(IsAuthenticated,),
        url_path='create'
    )
    def СreateCardForClient(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для создания карты.
        """
        serializer = CreateClientAndCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create_client_and_card(user=self.request.user)
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_201_CREATED)

    @action(
        detail=False, 
        methods=['GET'],
        permission_classes=(IsAuthenticated,),
        url_path='requisite'
    )
    def get_client_balance(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для получения баланса.
        """
        user = self.get_user(request=request)
        client: Client = Client.objects.get(user=user)
        serializer = RequisiteSerializer(client)
        response_data = serializer.data
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(IsAuthenticated,),
        url_path='fill_balance'
    )
    def fill_balance_transactions(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для перевода средств.
        """
        serializer = FillBalanceSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(IsAuthenticated,),
        url_path='refill'
    )
    def refil_transactions(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для перевода средств себе на карту.
        """
        serializer = RefillTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(IsAuthenticated,),
        url_path='transfer'
    )
    def transfer_transactions(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для перевода средств с карты.
        """
        serializer = TransferTransactionSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['GET'], 
        permission_classes=(IsAuthenticated,), 
        url_path='transactions'
    )
    def get_transactions(self, request: Request) -> JsonResponse:
        user = self.get_user(request=request)
        client = Client.objects.get(user=user)
        transactions = Transaction.objects.get_transactions_for_user(client)

        # Создаем экземпляр пагинатора
        paginator = TransactionPageNumberPaginator()

        # Получаем пагинированный queryset
        paginated_transactions = paginator.paginate_queryset(transactions, request)

        serializer = TransactionSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(AllowAny,),
        url_path='currency_create'
    )
    def СreateCurrency(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для получения актуальной валюты KZT to ... .
        """
        serializer = CreateCurrencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create_currecy()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_201_CREATED)

    @action(
        detail=False, 
        methods=['GET'],
        permission_classes=(AllowAny,),
        url_path='get_currency'
    )
    def get_exchange_rates(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для вывода актуальной валюты KZT to ... .
        """
        queryset = ExchangeRate.objects.all()
        serializer_class = ExchangeRateSerializer
        exchange_rates = queryset
        serializer = serializer_class(exchange_rates, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)