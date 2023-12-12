# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse

# Python
from typing import Callable


class SecureMiddleware:
    """
    Middleware для обеспечения безопасности.

    Устанавливает заголовки безопасности, такие как X-Frame-Options и X-Content-Type-Options.
    Также управляет установкой и удалением httponly cookie с токеном обновления (refresh_token).

    Attributes:
        LOGIN_REFERER (str): Ссылка для проверки Referer при логине.
        LOGOUT_REFERER (str): Ссылка для проверки Referer при логауте.

    Methods:
        __init__(self, get_response: Callable): Конструктор middleware.
        
        set_refresh_token_cookie(self, response: HttpResponse, token: str): 
        -> Устанавливает httponly cookie с токеном обновления.

        def delete_refresh_token_cookie(self, response: HttpResponse):
        -> Удаляет токен обновления при выходе пользователя с аккаунта.

        __call__(self, request: WSGIRequest) -> HttpResponse: Обработчик middleware.
    """

    # Ссылки для проверки Referer
    LOGIN_REFERER = 'http://127.0.0.1:8000/login/'
    LOGOUT_REFERER = 'http://127.0.0.1:8000/logout/'

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def set_refresh_token_cookie(self, response: HttpResponse, token: str) -> None:
        # Параметры для установки cookie
        params = {
            'httponly': True,
            'samesite': 'Strict',
            'path': '/'
        }

        # Определение срока действия токена
        expiration = 60 * 60 * 24 * 7  # 1 неделя
        expiration -= 60  # Вычесть одну минуту на всякий случай
        params['max_age'] = expiration

        # Установка cookie refresh_token
        response.set_cookie('refresh_token', token, **params)

    def delete_refresh_token_cookie(self, response: HttpResponse) -> None:
        """
        Удаление куки refresh_token из response.
        """
        # Параметры для удаления cookie
        params = {
            'path': '/',
        }

        # Удаление cookie refresh_token
        response.delete_cookie('refresh_token', **params)
        
    def __call__(self, request: WSGIRequest) -> HttpResponse:
        response = self.get_response(request)

        # Установка заголовков для защиты от XSS
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-Content-Type-Options'] = 'nosniff'

        # Установка httponly cookie refresh_token
        if request.META.get('HTTP_REFERER') == self.LOGIN_REFERER:
            # Если есть данные и ответ успешен (статус код 2xx)
            if hasattr(response, 'data') and 200 <= response.status_code < 300:
                refresh_token = response.data.get('refresh')
                # Если токен успешно получен
                if refresh_token:
                    self.set_refresh_token_cookie(response, refresh_token)

        # Удаление refresh_token из cookie
        elif request.META.get('HTTP_REFERER') == self.LOGOUT_REFERER:
            # Если есть данные и ответ успешен (статус код 200)
            if hasattr(response, 'data') and response.status_code == 200:
                self.delete_refresh_token_cookie(response)

        return response

