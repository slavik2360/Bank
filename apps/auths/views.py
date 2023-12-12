# Python
from typing import Optional

# DRF
from rest_framework.request import Request
from rest_framework.response import Response as JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# Local
from abstracts.mixins import (
    AccessTokenMixin,
    ObjectMixin
)
from auths.models import User
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
    UserCreateSerializer
)


class UserViewSet(AccessTokenMixin, ObjectMixin, ViewSet):
    """
    Представление для моделей Пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    )->JsonResponse:
        serializer: UserSerializer = \
            UserSerializer(
                instance=self.queryset,
                many=True
            )
        return JsonResponse(serializer.data)
    
    def retrieve(
        self,
        request:Request,
        pk: Optional[int] = None
    )->JsonResponse:
        user = self.get_object(self.queryset, pk)
        serializer = UserSerializer(user)
        return self.json_response(serializer.data)

    def create(
        self,
        request:Request,
        *args:tuple,
        **kwargs:dict
    )->JsonResponse:
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        return self.json_response(f'{user.title} is created. ID: {user.id}')

    def update(
        self,
        request:Request,
        pk: Optional[int] = None
    )->JsonResponse:
        user = self.get_object(self.queryset, pk)
        serializer = UserCreateSerializer(
            instance=user, 
            data=request.data
        )
        if not serializer.is_valid():
            return self.json_response(
                f'{user.title} wasn\'t updated', 'Warning'
            )
        user: User = serializer.save()
        return self.json_response(f'{user.title} was updated')

    def partial_update(
        self,
        request:Request,
    ) -> JsonResponse:
        user = self.get_user(request=request)
        serializer = self.serializer_class(instance=user)
        user = self.get_user()
        serializer = UserSerializer(
            instance=user, 
            data=request.data, 
            partial=True
        )
        if not serializer.is_valid():
            return self.json_response(
                f'{user.title} wasn\'t partially-updated', 'Warning'
            )
        user: User = serializer.save()
        return self.json_response(f'{user.title} was partially-updated')

    def destroy(
        self,
        request:Request,
        pk: Optional[int] = None,
        *args:tuple,
        **kwargs:dict
    )->JsonResponse:
        user = self.get_object(self.queryset, pk)
        name = user.title
        user.delete()
        return self.json_response(f'{name} was deleted')
    
    """
    API api/v1/auth/...
    """
    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(AllowAny,),
        url_path='register'
    )
    def register_user(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для регистрации пользователя.
        """
        serializer = RegistrateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_201_CREATED)

    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(AllowAny,),
        url_path='activate'
    )
    def activate_account(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для активации учетной записи пользователя после регистрации.
        """
        serializer = ActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(AllowAny,),
        url_path='login'
    )
    def login_user(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для входа пользователя в систему.
        """
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(AllowAny,),
        url_path='login/token'
    )
    def refresh_token(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для обновления токена доступа пользователя.
        """
        serializer = RefreshTokenSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['post'],
        permission_classes=(AllowAny,),
        url_path='change'
    )
    def change_password(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для изменения пароля пользователя.
        """
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(AllowAny,),
        url_path='forgot-password'
    )
    def forgot_password(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для запроса сброса пароля пользователя.
        """
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(AllowAny,),
        url_path='reset-password'
    )
    def reset_password(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для подтверждения смены пароля пользователя.
        """
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['GET'],
        permission_classes=(IsAuthenticated,),
        url_path='user'
    )
    def get_user_data(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для получения данных о пользователе.
        Доступ только при авторизации.
        """
        user = self.get_user(request=request)
        serializer = self.serializer_class(instance=user)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(
        detail=False,
        methods=['patch'],
        permission_classes=[IsAuthenticated],
        url_path='update-avatar'
    )
    def update_avatar(self, request: Request):
        user = self.get_user(request=request)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['GET'],
        permission_classes=(AllowAny,),
        url_path='is-auth'
    )
    def is_authenticated(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для подтверждения аутентификации пользователя.
        """
        # Получение refresh_token
        refresh_token = request.COOKIES.get('refresh_token')

        # Проверка, есть ли токен обновления
        if not check_refresh_token(refresh_token=refresh_token):
            return JsonResponse(status=400)

        return JsonResponse(status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['POST'],
        permission_classes=(AllowAny,),
        url_path='logout'
    )
    def logout(self, request: Request) -> JsonResponse:
        """
        Эндпойнт для выхода пользователя из системы.
        """
        serializer = LogoutSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.build_response()
        return JsonResponse(response_data, status=status.HTTP_200_OK)

