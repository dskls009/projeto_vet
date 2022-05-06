from commons.models import Usuario
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, Http404, JsonResponse
import json
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django import setup
from django.core.management import call_command
from django.db.models import Q


def upgrade():
    """
    executa a migração do banco, atualização
    """
    setup()
    call_command('migrate', '--database=default', interactive=False)


@csrf_exempt
def login(request):
    """
    executa o login e atribui o usuário logado a sessão do cliente
    """
    body = json.loads(request.body.decode('utf-8'))
    upgrade()
    from rest_framework_jwt.settings import api_settings
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    from django.contrib.auth.models import User
    from django.contrib.auth.hashers import make_password
    from django.conf import settings
    try:
        usuario = User.objects.get(username=body['username'], password=make_password(
            password=body['password'], salt=settings.SECRET_KEY, hasher='pbkdf2_sha256'))
    except Usuario.DoesNotExist as error:
        raise Http404('Usuário não encontrado')
    payload = jwt_payload_handler(usuario)
    token = jwt_encode_handler(payload)

    return JsonResponse({'token': "jwt {}".format(token), 'fullname': usuario.first_name+' '+usuario.last_name})