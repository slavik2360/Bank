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
from abstracts.mixins import (
    AccessTokenMixin,
    ObjectMixin
)
from bank.models import (
    Client,
    Card,
    Transaction
)
from bank.serializers import (
    ClientSerializer,
    CreateClientAndCardSerializer,
    ForMeTransactionSerializer,
    ForYouTransactionSerializer
    # CardSerializer
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
        serializer = ClientSerializer(client)
        response_data = serializer.data
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(IsAuthenticated,),
        url_path='forme_transaction'
    )
    def forme_transactions(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для перевода средств себе на карту.
        """
        serializer = ForMeTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(IsAuthenticated,),
        url_path='foryou_transaction'
    )
    def foryou_transactions(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для перевода средств с карты.
        """
        serializer = ForYouTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)

# class CLSss:
#     serializer_class = ClientSerializer
#     queryset = Client.objects.all()

#     def list(
#         self,
#         request: Request,
#         *args: tuple,
#         **kwargs: dict
#     )->JsonResponse:
#         serializer: ClientSerializer = \
#             ClientSerializer(
#                 instance=self.queryset,
#                 many=True
#             )
#         return JsonResponse(serializer.data)
    
    # serializer = ChangePasswordSerializer(
    #         data=request.data, 
    #         context={'request': request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     response_data = serializer.get_response()
    #     return JsonResponse(response_data, status=status.HTTP_200_OK)