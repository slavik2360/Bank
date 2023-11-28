# Python
from typing import Any

# DRF
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from settings import base
from django.template.loader import render_to_string

# Local
from auths.models import User, AccountCode


@receiver(signal=post_save, sender=User)
def user_post_save(
    sender: User.__class__, 
    instance: User, 
    created: bool, 
    **kwargs: Any
) -> None:
    if created:
        # Хэширование пароля пользователя
        instance.set_password(instance.password)
        instance.password2 = instance.password
        instance.save(update_fields=('password', 'password2'))
        print('Пароль успешно захеширован')


@receiver(signal=pre_save, sender=AccountCode)
def accountcode_pre_save(instance: AccountCode, **kwargs: Any) -> None:
    """
    Отправка кода активации учетной записи по электронной почте 
    пользователю после регистрации.
    """
    # User
    user: User = instance.user

    # Проверка типа кода
    if instance.code_type == AccountCode.ACCOUNT_ACTIVATION:
        # Тема письма
        subject: str = 'Активация Аккаунта'
        # Тело письма для активации аккаунта
        context = {
            'user_fullname': user.fullname,
            'activation_code': instance.code,
            'activation_link': f'http://127.0.0.1:8000/activate/{user.email}/',
        }
        message: str = render_to_string('activation_email_message.html', context)

    elif instance.code_type == AccountCode.PASSWORD_RESET:
        # Тема письма
        subject: str = 'Восстановление пароля'
        # Тело письма для сброса пароля
        context = {
            'user_fullname': user.fullname,
            'activation_code': instance.code,
        }
        message: str = render_to_string('fogot_password_message.html', context)

    # Отправка сообщения
    send_mail(
        subject=subject,
        message=message,
        from_email=base.EMAIL_FROM,
        recipient_list=[user.email],
        html_message=message,
    )
    print(f"Сообщение отправлено {user.email}")