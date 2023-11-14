# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Local
from auths.serializers import (
    RegistrateUserSerializer,
    LoginUserSerializer,
    ActivateAccountSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ConfirmPasswordSerializer,
    RefreshTokenSerializer,
    LogoutSerializer,
    UserSerializer,
)

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegistrateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)

class ActivateAccountView(APIView):
    def post(self, request):
        serializer = ActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)

class ConfirmPasswordView(APIView):
    def post(self, request):
        serializer = ConfirmPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)

class RefreshTokenView(APIView):
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)

class UserView(APIView):
    def get(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        response_data = serializer.get_response()
        return Response(response_data, status=status.HTTP_200_OK)
