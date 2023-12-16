# Django
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import render


class BaseView(View):
    """
    Базовое представление, для html страниц.
    """

    template: str = ''

    def get(
        self, 
        request: WSGIRequest,
        *args: tuple, 
        **kwargs: dict
    ) -> HttpResponse:
        """
        Метод, GET.
        """
        refresh_token_exists = 'refresh_token' in request.COOKIES
        return render(
            request=request, 
            template_name=self.template,
            context={'refresh_token_exists': refresh_token_exists}
        )
    

class HomePageView(BaseView):
    """
    Домашняя страница.
    """

    template: str = 'nimbus.html'


class RegistrationView(BaseView):
    """
    Страница Регистрации.
    """

    template: str = 'registration.html'


class LoginView(BaseView):
    """
    Авторизация пользователя.
    """

    template: str = 'login.html'


class ActivationBaseView(BaseView):
    """
    Activate user account.
    """

    template: str = 'base_activate.html'


class AccountActivationView(BaseView):
    """
    Активация учетной записи пользователя.
    """

    template: str = 'activate_account.html'


class ForgotPasswordView(BaseView):
    """
    Восстановление пароля.
    """

    template: str = 'forgot-password.html'


class ResetPasswordView(BaseView):
    """
    Смена пароля.
    """

    template: str = 'reset-password.html'


class ProfileView(BaseView):
    """
    Профиль пользователя.
    """

    template: str = 'profile.html'


class FillWalletView(BaseView):
    """
    Пополнение кошелька.
    """

    template: str = 'fill_wallet.html'


class TransferView(BaseView):
    """
    Перевод денег с карты.
    """

    template: str = 'transfer.html'


class RefillView(BaseView):
    """
    Перевод денег на карту.
    """

    template: str = 'refill.html'


class HistoryTransferView(BaseView):
    """
    История транзакций по карте.
    """

    template: str = 'history_transfer.html'


class ReqisiteCardView(BaseView):
    """
    Получения реквизитов карты.
    """

    template: str = 'requisite_card.html'


class ConvertCurrencyView(BaseView):
    """
    Конвертация валюты.
    """

    template: str = 'convert_currency.html'


class CurrenciesView(BaseView):
    """
    Курс валют.
    """

    template: str = 'currencies.html'


class NimbusAdsView(BaseView):
    """
    Магазин товаров.
    """

    template: str = 'ads_nimbus.html'


class CreateAdsView(BaseView):
    """
    Белый список/Избранное.
    """

    template: str = 'ads_create.html'


class HistoryAdsView(BaseView):
    """
    История объявлений.
    """

    template: str = 'ads_history.html'