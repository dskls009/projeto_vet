from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('commons.urls')),
    path('api/veterinaria/', include('veterinaria.urls')),
    path('api/relatorios/', include('relatorios.urls')),
    # path('/api/petshop', include('petshop.urls')),
    # path('/api/financeiro', include('financeiro.urls')),
    path('admin/', admin.site.urls),
]
