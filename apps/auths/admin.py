# Python
# from typing import Optional

# # Django
from django.contrib import admin

# Local
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    UserAdmin admin.
    """
    readonly_fields = ()