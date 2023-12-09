# DRF
from django.contrib import admin

# Local
from bank.models import (
    Client,
    Card,
    Transaction,
    ExchangeRate
)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    ClientAdmin admin.
    """
    readonly_fields = ()

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """
    CardAdmin admin.
    """
    readonly_fields = ()

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    TransactionAdmin admin.
    """
    readonly_fields = ()

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    """
    ExchangeRateAdmin admin.
    """
    readonly_fields = ()