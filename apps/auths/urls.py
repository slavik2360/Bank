# DRF
from django.urls import path

#local
from .views import (
    RegisterUserView,      
    LoginUserView,         
    ActivateAccountView,  
    ChangePasswordView,    
    ForgotPasswordView,    
    ConfirmPasswordView,   
    RefreshTokenView,      
    LogoutView,
    IsAuthView,            
    UserView,       
)

urlpatterns = [
    # Регистрация нового пользователя
    path('register/', RegisterUserView.as_view(), name='register'),
    # Вход пользователя в систему
    path('login/', LoginUserView.as_view(), name='login'),
    # Активация учетной записи пользователя
    path('activate/', ActivateAccountView.as_view(), name='activate'),
    # Изменение пароля пользователя
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # Запрос на сброс пароля пользователя
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    # Подтверждение смены пароля пользователя
    path('confirm-password/', ConfirmPasswordView.as_view(), name='confirm-password'),
    # Обновление токена доступа
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    # Выход пользователя из системы
    path('logout/', LogoutView.as_view(), name='logout'),
    # Если пользователь был аутентифицирован
    path('authentication/', IsAuthView.as_view(), name='is-auth'),
    # Получение данных о пользователе
    path('user/', UserView.as_view(), name='user'),
]
