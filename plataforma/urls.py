from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import EventoCreateView, sucesso, download_contrato

urlpatterns = [
    path('', EventoCreateView.as_view(), name='criar_evento'),
    path('sucesso/', sucesso, name='sucesso'),
    path('download_contrato/', download_contrato, name='download_contrato'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
