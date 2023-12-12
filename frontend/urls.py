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
    FillWalletView,
    TransferView,
    RefillView,
    HistoryTransferView,
    ReqisiteCardView,
    ConvertCurrencyView,
    CurrenciesView,
    NinbusStoreView,
    WhiteListView,
    ShoppingСartView,
    HistoryPayView
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

    # Обменный курс
    path('currencies/', CurrenciesView.as_view()),

    # Перевод на карту
    path('fill_wallet/', FillWalletView.as_view()),

    # Перевод на карту
    path('transfer/', TransferView.as_view()),

    # Пополнение карты
    path('refill/', RefillView.as_view()),

    # История транзакций
    path('history-transfer/', HistoryTransferView.as_view()),

    # Реквизиты карты
    path('requisite/', ReqisiteCardView.as_view()),

    # Конвертация валюты
    path('convert/', ConvertCurrencyView.as_view()),

    # # 
    # path('/', .as_view()),

    # # 
    # path('/', .as_view()),

    # # 
    # path('/', .as_view()),

    # # 
    # path('/', .as_view()),

    # # 
    # path('/', .as_view()),
]