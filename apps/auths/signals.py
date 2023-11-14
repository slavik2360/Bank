# Python
from typing import Any

# DRF
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from settings import base
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Local
from auths.models import User, AccountCode


# @receiver(signal=post_save, sender=User)
# def send_activation_email(
#     sender: User.__class__, 
#     instance: User, 
#     created: bool, 
#     **kwargs: Any
# ) -> None:
#     if created:
#         activation_code = AccountCode.objects.create(
#             user=instance,
#             code_type=AccountCode.ACCOUNT_ACTIVATION
#         )

#         subject = 'Активируйте вашу учетную запись'
#         message = render_to_string('activation_email_template.html', {
#             'user': instance,
#             'activation_code': activation_code.code,
#         })
#         plain_message = strip_tags(message)
#         from_email = settings.DEFAULT_FROM_EMAIL
#         to_email = instance.email
#         send_mail(subject, plain_message, from_email, [to_email], html_message=message)


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
        print('signal_user_post_save')


# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     """
#     Отправка приветственного электронного письма при успешной регистрации.
#     """
#     print('сигнал с emailom ')
#     if created:
#         subject = 'Добро пожаловать!'
#         message = render_to_string('welcome_email.txt', {'user': instance})
#         from_email = settings.DEFAULT_FROM_EMAIL
#         to_email = [instance.email]

#         send_mail(subject, message, from_email, to_email)





@receiver(pre_save, sender=AccountCode)
def accountcode_pre_save(instance: AccountCode, **kwargs: Any) -> None:
    """
    Send account activation code by email to the user after registration.
    """
    # User
    user: User = instance.user

    # Проверка типа кода
    if instance.code_type == AccountCode.ACCOUNT_ACTIVATION:

        subject: str = 'Активация Аккаунта'
        message: str = (
            'Дорогой %s,\n\n'
            'Мы рады приветствовать вас и сообщаем вам '
            'об успешной регистрации.'
            '\nВаш, код активации ниже:\n\nКод активации: %s\n\n'
            'Для завершения регистрации перейдите по\n'
            'следующей ссылке: http://127.0.0.1:8000/activate/%s/'
            '\n\nПосле перехода по ссылке вы будете перенаправлены на '
            'наш веб-сайт, где сможете ввести\nкод активации и '
            'продолжить пользоваться нашей платформой.\n\nЕсли у вас есть вопросы '
            'или вам нужна помощь, не стесняйтесь обращаться в нашу'
            'службу поддержки .\n\n'
            'Еще раз спасибо, что выбрали нас.'
        ) % (user.fullname, instance.code, user.email)

    elif instance.code_type == AccountCode.PASSWORD_RESET:
        # Тема письма для сброса пароля
        subject: str = 'Восстановление пароля'

        # Тело письма для сброса пароля
        message: str = (
            'Привет, %s.\n'
            'Введите этот код на сайте для сброса пароля:\n'
            '%s\n'
            'Если это были не вы, просто проигнорируйте это сообщение.'
            % (user.fullname, instance.code)
        )

    # Отправка сообщения
    send_mail(
        subject=subject,
        message=message,
        from_email=base.EMAIL_FROM,
        recipient_list=[user.email],
    )
    print(f"Сообщение отправлено {user.email}")

