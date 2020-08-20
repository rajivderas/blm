from django.contrib import admin

from .models import Team, Coach

# Register your models here.
models = [Team, Coach]
admin.site.register(models)