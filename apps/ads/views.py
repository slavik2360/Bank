# Python
from typing import Optional, Any

# DRF
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response as JsonResponse 
from rest_framework.permissions import IsAuthenticated, AllowAny

# Local 
from bank.models import Client
from abstracts.mixins import AccessTokenMixin
from bank.paginators import TransactionPageNumberPaginator
from ads.models import (
    Ads,
    AdHistory
)
from ads.serializers import (
    AdsSerializer,
    AdsCreateSerializer,
    AdsTakeJobSerializer,
    AdsCompleteJobSerializer,
    AdHistorySerializer
)


class AdsCreateView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        serializer = AdsCreateSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_201_CREATED)


class AdsTakeJobView(APIView, AccessTokenMixin):
    
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        ad_id = kwargs.get('ad_id')
        user = self.get_user(request=request)

        acting_client: Client = Client.objects.get(user=user)

        try:
            ad = Ads.objects.get(pk=ad_id)
        except Ads.DoesNotExist:
            return JsonResponse({'error': 'Объявление не найдено'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, что текущий пользователь не является владельцем объявления
        if ad.customer == acting_client:
            return JsonResponse(
                {'error': 'Нельзя принять свое собственное объявление'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AdsTakeJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(ad=ad, acting_client=acting_client)

        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    

class AdsCompleteJobView(APIView, AccessTokenMixin):

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        ad_id = kwargs.get('ad_id')
        user = self.get_user(request=request)
        acting_client: Client = Client.objects.get(user=user)

        try:
            ad = Ads.objects.get(pk=ad_id)
        except Ads.DoesNotExist:
            return JsonResponse({'error': 'Объявление не найдено'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdsCompleteJobSerializer(data={})
        serializer.is_valid(raise_exception=True)

        # Проверка, что текущий пользователь - заказчик этого объявления
        if ad.customer != acting_client:
            return JsonResponse({'error': 'Вы не являетесь заказчиком этого объявления'}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(ad=ad, acting_client=acting_client)

        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)


class AdsListView(generics.ListAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    

class AdHistoryListView(AccessTokenMixin, generics.ListAPIView):
    serializer_class = AdHistorySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = TransactionPageNumberPaginator

    def get_queryset(self):
        user = self.get_user(request=self.request)
        queryset = AdHistory.objects.filter(client__user=user)

        return queryset