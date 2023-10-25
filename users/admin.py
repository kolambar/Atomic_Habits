from django.contrib import admin

from users.models import User


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'telegram', 'telegram_id', )
    search_fields = ('email', 'telegram', )
