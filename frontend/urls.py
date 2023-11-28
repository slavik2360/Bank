# Django
from django.urls import path

# Local
from .views import (
    HomePageView,
    RegistrationView,
    # AccountActivationView,
    # AccountActivationBaseView,
    # LoginView,
    # InformationView,
    # ForgotPasswordView,
    # ProfileView,
    # ReplenishBalanceView,
    # NewPasswordView,
    # TransactionView,
    # TransactionAllView,
    # WithdrawMoneyView,
    # CurrencyConvertationView,
)

urlpatterns = [
    # Домашняя страница
    path('', HomePageView.as_view(), name='homepage'),

    # Регистрация
    path('registration/', RegistrationView.as_view(), name='registration')
]