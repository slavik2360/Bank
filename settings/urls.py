# DRF
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Local
from auths.views import UserViewSet

router = DefaultRouter()

# Роут API обработки для Авторизации
router.register(r'auth', UserViewSet, basename='auth')


urlpatterns = [
    # Панель Администратора
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Роут для пользовательской API обработки
    path('api/v1/', include(router.urls)),

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
