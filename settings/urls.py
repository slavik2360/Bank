from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


# from bank.views import BankViewSet


router = DefaultRouter()
# router.register(r'game', GameViewSet)

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

urlpatterns += [
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]