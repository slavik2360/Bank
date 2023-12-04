from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # Панель Администратора
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Пользовательская API обработка для Авторизации
    path('api/v1/auth/', include('auths.urls')),

    # Пользовательская API обработка для Банка
    # path('api/v1/bank/', include('bank.urls')),

    # Роут для предтавления страниц на сайте
    path("", include('frontend.urls')),

]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
