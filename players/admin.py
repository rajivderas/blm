from django.contrib import admin

from .models import Player, Role, UserRole

# Register your models here.
models = [Player, Role, UserRole]
admin.site.register(models)
