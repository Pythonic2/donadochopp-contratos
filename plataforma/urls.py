from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('get-cliente', get_cliente, name='get-cliente'),
    path('criar-evento/<int:id_cliente>/', EventoCreateView.as_view(), name='criar-evento'),
    path('add-produto/<int:id_evento>/', AddProduto.as_view(), name='add-produto'),
    path('finalizar-contrato/<int:id_evento>/', finalizar_contrato, name='finalizar-contrato'),
    path('cadastrar-cliente/', CreateCliente.as_view(), name='cadastrar-cliente'),
    path('cadastrar-produto/', CreateProduto.as_view(), name='cadastrar-produto'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
