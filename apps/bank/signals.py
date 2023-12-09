from django.db.models.signals import post_save
from django.dispatch import receiver
from auths.models import User
from .models import Client

# Сигнал для создания клиента при создании пользователя
@receiver(post_save, sender=User)
def create_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)

# Сигнал для сохранения клиента при сохранении пользователя
@receiver(post_save, sender=User)
def save_client(sender, instance, **kwargs):
    instance.client.save()