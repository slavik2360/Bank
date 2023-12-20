# DRF
from celery import shared_task
from django.utils import timezone
# Local 
from bank.models import Card

@shared_task
def delete_expired_cards():
    expired_cards = Card.objects.filter(date_expiration__lt=timezone.now())
    expired_cards.delete()