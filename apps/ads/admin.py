# DRF
from django.contrib import admin

# Local
from ads.models import (
    Ads,
    AdHistory
)


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    """
    AdsAdmin admin.
    """
    readonly_fields = ()


@admin.register(AdHistory)
class AdHistoryAdmin(admin.ModelAdmin):
    """
    TransactionAdmin admin.
    """
    readonly_fields = ()


