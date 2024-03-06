from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mygreatproject.models.user import User


@admin.register(User)
class MyGreatProjectUserAdmin(UserAdmin):
    # special admin class for User model, normally these use django ModelAdmin
    pass
