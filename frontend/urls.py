# Django
from django.urls import path

# Local
from .views import (
    HomePageView,
    RegistrationView,
    AccountActivationView,
    LoginView,
    ForgotPasswordView,
    ResetPasswordView,
    ProfileView,
)

urlpatterns = [
    # Домашняя страница
    path('', HomePageView.as_view(), name='homepage'),

    # Регистрация
    path('registration/', RegistrationView.as_view(), name='registration'),

    # Авторизация пользователя
    path('login/', LoginView.as_view()),
   
    # Активация аккаунта
    path('account/activate/<str:email>/', AccountActivationView.as_view()),

    # Забыли пароль
    path('forgot-password/', ForgotPasswordView.as_view()),
    
    # Смена пароля пользователя
    path('reset-password/<str:email>/', ResetPasswordView.as_view()), 

    # Профиль пользователя
    path('account/', ProfileView.as_view()),
]