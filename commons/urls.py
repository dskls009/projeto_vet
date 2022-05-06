from django.urls.conf import include
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from .repository.login import login
from .repository import animal_repository, cliente_repository, base64_repository

urlpatterns = [
    path('api/login', login),
    path('api/token/', obtain_jwt_token),
    path('api/token/verify/', verify_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),
    path('api/cliente', cliente_repository.clientes_findall),
    path('api/cliente/<int:pk>', cliente_repository.cliente_get),
    path('api/cliente/<int:pk>/edit', cliente_repository.cliente_edit),
    path('api/cliente/create', cliente_repository.cliente_create),
    path('api/cliente/<int:pk>/delete', cliente_repository.cliente_delete),
    path('api/animal', animal_repository.animais_findall),
    path('api/animal/<int:pk>', animal_repository.animal_get),
    path('api/animal/<int:pk>/edit', animal_repository.animal_edit),
    path('api/animal/create', animal_repository.animal_create),
    path('api/animal/<int:pk>/delete', animal_repository.animal_delete),
    path('api/base64', base64_repository.base64_findall),
    path('api/base64/<int:pk>', base64_repository.base64_get),
    path('api/base64/<int:pk>/download', base64_repository.base64_download),
    path('api/base64/<int:pk>/edit', base64_repository.base64_edit),
    path('api/base64/create', base64_repository.base64_create),
    path('api/base64/<int:pk>/delete', base64_repository.base64_delete),
]