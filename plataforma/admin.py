from django.contrib import admin

# Register your models here.
from .models import Evento, Cliente, Produto, EventoProduto

admin.site.register(Evento)
admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(EventoProduto)