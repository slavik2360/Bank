# # DRF
# from django.urls import path

# #local
# from .views import (
#     RegisterUserView,      
#     LoginUserView,         
#     ActivateAccountView,    
#     ForgotPasswordView,    
#     ResetPasswordView,   
#     RefreshTokenView,      
#     LogoutView,
#     IsAuthView,            
#     UserView,       
# )

# urlpatterns = [
#     # Регистрация нового пользователя
#     path('register/', RegisterUserView.as_view()),
#     # Активация учетной записи пользователя
#     path('activate/', ActivateAccountView.as_view()),
#     # Вход пользователя в систему
#     path('login/', LoginUserView.as_view()),
#     # Обновление токена доступа
#     path('login/token/', RefreshTokenView.as_view()),
#     # Запрос на сброс пароля пользователя
#     path('forgot-password/', ForgotPasswordView.as_view()),
#     # Подтверждение смены пароля пользователя
#     path('reset-password/', ResetPasswordView.as_view()),
#     # Проверка сли пользователь аутентифицирован
#     path('is-auth/', IsAuthView.as_view(), name='is-auth'),
#     # Получение данных о пользователе
#     path('user/', UserView.as_view()),
#     # Выход пользователя из системы
#     path('logout/', LogoutView.as_view()),
# ]
