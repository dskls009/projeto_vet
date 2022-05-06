from django.urls.conf import include
from django.urls import path
from .repository import relatorio_repository


urlpatterns = [
    path('cliente', relatorio_repository.clientes_relatorio),
    path('animal', relatorio_repository.animais_relatorio),
]