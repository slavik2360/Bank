from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import User, AccountCode

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        activation_code = AccountCode.objects.create(
            user=instance,
            code_type=AccountCode.ACCOUNT_ACTIVATION
        )

        subject = 'Активируйте вашу учетную запись'
        message = render_to_string('activation_email_template.html', {
            'user': instance,
            'activation_code': activation_code.code,
        })
        plain_message = strip_tags(message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.email
        send_mail(subject, plain_message, from_email, [to_email], html_message=message)
