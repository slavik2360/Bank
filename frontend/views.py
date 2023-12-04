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
        return render(request=request, template_name=self.template)
    

class HomePageView(BaseView):
    """
    Домашняя страница.
    """

    template: str = 'home.html'


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