from django.contrib import admin
from authentication.models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ("username", "date_of_birth")


admin.site.register(User, UserAdmin)
