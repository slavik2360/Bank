# DRF
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

# Local
from abstracts.mixins import AccessTokenMixin
from auths.services.token_utils import check_refresh_token
from auths.serializers import (
    RegistrateUserSerializer,
    LoginUserSerializer,
    ActivateAccountSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    RefreshTokenSerializer,
    LogoutSerializer,
    UserSerializer,
)

class RegisterUserView(APIView):
    """
    Эндпойнт для регистрации пользователя.
    """
    def post(self, request: Request) -> Response:
        serializer = RegistrateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_201_CREATED)
    

class ActivateAccountView(APIView):
    """
    Эндпойнт для активации учетной записи пользователя после регистрации.
    """
    def post(self, request: Request) -> Response:
        serializer = ActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)


class LoginUserView(APIView):
    """
    Эндпойнт для входа пользователя в систему.
    """
    def post(self, request: Request) -> Response:
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    Эндпойнт для обновления токена доступа пользователя.
    """
    def post(self, request: Request) -> Response:
        serializer = RefreshTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)
    

class ChangePasswordView(APIView):
    """
    Эндпойнт для изменения пароля пользователя.
    """
    def post(self, request: Request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    """
    Эндпойнт для запроса сброса пароля пользователя.
    """
    def post(self, request: Request) -> Response:
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """
    Эндпойнт для подтверждения смены пароля пользователя.
    """
    def post(self, request: Request) -> Response:
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)


class UserView(GenericAPIView, AccessTokenMixin):
    """
    Эндпойнт для получения данных о пользователе.
    Доступ только при авторизации.
    """

    permission_classes: tuple = (IsAuthenticated,)
    serializer_class: UserSerializer = UserSerializer
    success_status: int = 200

    def get(self, request: Request) -> Response:
        """
        GET запрос.
        """
        user = self.get_user(request=request)
        serializer = self.serializer_class(instance=user)
        return Response(data=serializer.data, status=self.success_status)


class IsAuthView(GenericAPIView, AccessTokenMixin):
    """
    Эндпойнт для подтверки аутентификации пользователя.
    """

    permission_classes: tuple = (AllowAny,)
    success_status: int = 200

    def get(self, request: Request) -> Response:
        """
        GET запрос.
        """
        # Получение refresh_token
        refresh_token: str = request.COOKIES.get('refresh_token')

        # Проверка, есть ли токен обновления
        if check_refresh_token(refresh_token=refresh_token) is False:
            return Response(status=400)

        return Response(status=self.success_status)
    

class LogoutView(APIView):
    """
    Эндпойнт для выхода пользователя из системы.
    """
    def post(self, request: Request) -> Response:
        serializer = LogoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.build_response()
        return Response(response_data, status=status.HTTP_200_OK)