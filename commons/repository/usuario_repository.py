from django.shortcuts import get_object_or_404
from django.utils import timezone  # pega data e hora com fuso horário
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
import json
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from commons.models import Endereco, Usuario

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def usuarios_findall(request):
    filtro = request.GET.get('filtro', None)

    usuarios = Usuario.objects

    if filtro:
        usuarios = usuarios.filter(
            Q(nome__icontains=filtro)
            | Q(crmv__icontains=filtro)
            | Q(sobrenome__icontains=filtro)
            | Q(cpf__icontains=filtro)
            | Q(email__icontains=filtro)
            | Q(telefone_1__icontains=filtro)
            | Q(telefone_2__icontains=filtro)
        )

    usuarios = usuarios.all().values('id', 'cpf', 'nome', 'sobrenome', 'email', 'telefone_1', 'telefone_2')

    if usuarios:
        usuarios = list(usuarios)
    else:
        usuarios = ()

    return JsonResponse({'data':usuarios}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def usuario_get(request, pk):
    try:
        usuario = Usuario.objects.filter(pk=pk).all().values('id', 'cpf', 'nome', 'sobrenome', 'email', 'telefone_1', 'telefone_2')
        if not usuario:
            raise Http404('Usuario não encontrado.')
        return JsonResponse(usuario[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def usuario_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            usuario = Usuario()
            usuario.criado_por = request.user.id
            usuario.criado_em = timezone.now()
            usuario.crmv = body.get('crmv', None)
            usuario.foto = body.get('foto', None)
            usuario.nome = body.get('nome', None)
            usuario.sobrenome = body.get('sobrenome', None)
            usuario.cpf = body.get('cpf', None)
            usuario.email = body.get('email', None)
            usuario.telefone_1 = body.get('telefone_1', None)
            usuario.telefone_2 = body.get('telefone_2', None)
            endereco = Endereco()
            usuario.endereco = endereco
            endereco.endereco = body.get('endereco__endereco', None)
            endereco.numero = body.get('endereco__numero', None)
            endereco.complemento = body.get('endereco__complemento', None)
            endereco.bairro = body.get('endereco__bairro', None)
            endereco.municipio = body.get('endereco__municipio', None)
            endereco.estado = body.get('endereco__estado', None)
            endereco.cep = body.get('endereco__cep', None)
            endereco.criado_em = timezone.now()
            endereco.criado_por = request.user.id
            endereco.save()
            usuario.save()
            return JsonResponse({'status':True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def usuario_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            usuario = get_object_or_404(Usuario, pk=pk)
            usuario.alterado_em = timezone.now()
            usuario.alterado_por = request.user.id
            usuario.crmv = body.get('crmv', None)
            usuario.foto = body.get('foto', None)
            usuario.nome = body.get('nome', None)
            usuario.sobrenome = body.get('sobrenome', None)
            usuario.cpf = body.get('cpf', None)
            usuario.email = body.get('email', None)
            usuario.telefone_1 = body.get('telefone_1', None)
            usuario.telefone_2 = body.get('telefone_2', None)
            endereco = Endereco()
            if body.get('endereco__id', None):
                endereco = get_object_or_404(Endereco, pk=body.get('endereco__id', None))
                endereco.alterado_em = timezone.now()
                endereco.alterado_por = request.user.id
            else:
                endereco.criado_em = timezone.now()
                endereco.criado_por = request.user.id
            usuario.endereco = endereco
            endereco.endereco = body.get('endereco__endereco', None)
            endereco.numero = body.get('endereco__numero', None)
            endereco.complemento = body.get('endereco__complemento', None)
            endereco.bairro = body.get('endereco__bairro', None)
            endereco.municipio = body.get('endereco__municipio', None)
            endereco.estado = body.get('endereco__estado', None)
            endereco.cep = body.get('endereco__cep', None)
            endereco.save()
            usuario.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def usuario_delete(request, pk):
    try:
        usuario = get_object_or_404(Usuario, pk=pk)
        usuario.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
