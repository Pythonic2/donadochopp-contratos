from django.contrib import admin

# Register your models here.
from .models import Evento, ContratoPadrao

admin.site.register(Evento)
admin.site.register(ContratoPadrao)
