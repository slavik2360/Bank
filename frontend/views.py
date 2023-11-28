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
        request: WSGIRequest
    ) -> HttpResponse:
        """
        Метод, GET.
        """
        return render(request=request, template_name=self.template)
    

class HomePageView(BaseView):
    """
    Домашняя страница.
    """

    template: str = 'index.html'
    
class RegistrationView(BaseView):
    """
    Страница Регистрации
    """

    template: str = 'registration.html'