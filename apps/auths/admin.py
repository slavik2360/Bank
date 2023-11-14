# DRF
from django.contrib import admin

# Local
from auths.models import (
    User,
    AccountCode,
    TokenList
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User admin.
    """
    # all_user_fields: tuple = ('email', 'first_name', 'last_name',
    #                           'is_active', 'is_staff', 'is_superuser')
    # fields = all_user_fields

    # list_display = all_user_fields

    # list_filter = all_user_fields[3:6]

    # readonly_fields = all_user_fields
    readonly_fields = ()


@admin.register(AccountCode)
class AccountCodeAdmin(admin.ModelAdmin):
    """
    AccountCode admin.
    """
    readonly_fields = ()


@admin.register(TokenList)
class TokenListAdmin(admin.ModelAdmin):
    """
    TokenList admin.
    """
    readonly_fields = ()