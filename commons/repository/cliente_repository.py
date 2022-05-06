from django.shortcuts import get_object_or_404
from django.utils import timezone  # pega data e hora com fuso horário
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
import json
import pandas as pd
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from commons.models import Endereco, Cliente
from django.core.files.storage import Storage


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def clientes_findall(request):
    filtro = request.GET.get('filtro', None)

    clientes = Cliente.objects

    if filtro:
        clientes = clientes.filter(
            Q(nome__icontains=filtro)
            | Q(sobrenome__icontains=filtro)
            | Q(cpf__icontains=filtro)
            | Q(email__icontains=filtro)
            | Q(telefone_1__icontains=filtro)
            | Q(telefone_2__icontains=filtro)
        )

    if filtro and filtro.lower() == 'inadimplente':
        clientes = clientes.filter(inadimplente=True)

    clientes = clientes.all().values('id',
                                     'foto',
                                     'genero',
                                     'inadimplente',
                                     'cpf',
                                     'nome',
                                     'sobrenome',
                                     'email',
                                     'telefone_1',
                                     'telefone_2',
                                     'endereco__id',
                                     'endereco__cep',
                                     'endereco__endereco',
                                     'endereco__numero',
                                     'endereco__complemento',
                                     'endereco__bairro',
                                     'endereco__municipio',
                                     'endereco__estado')

    if clientes:
        clientes = list(clientes)
    else:
        clientes = ()

    return JsonResponse({'data': clientes}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def cliente_get(request, pk):
    try:
        cliente = Cliente.objects.filter(pk=pk).all().values('id',
                                     'foto',
                                     'genero',
                                     'inadimplente',
                                     'cpf',
                                     'nome',
                                     'sobrenome',
                                     'email',
                                     'telefone_1',
                                     'telefone_2',
                                     'endereco__id',
                                     'endereco__cep',
                                     'endereco__endereco',
                                     'endereco__numero',
                                     'endereco__complemento',
                                     'endereco__bairro',
                                     'endereco__municipio',
                                     'endereco__estado')
        if not cliente:
            raise Http404('Cliente não encontrado.')
        return JsonResponse(cliente[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def cliente_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            cliente = Cliente()
            cliente.criado_por = request.user.id
            cliente.criado_em = timezone.now()
            cliente.foto = body.get('foto', None)
            cliente.nome = body.get('nome', None)
            cliente.genero = body.get('genero', None)
            cliente.sobrenome = body.get('sobrenome', None)
            cliente.cpf = body.get('cpf', None)
            cliente.email = body.get('email', None)
            cliente.telefone_1 = body.get('telefone_1', None)
            cliente.telefone_2 = body.get('telefone_2', None)
            cliente.inadimplente = body.get('inadimplente', None)
            if body.get('endereco__endereco', None):
                endereco = Endereco()
                cliente.endereco = endereco
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
            cliente.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def cliente_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            cliente = get_object_or_404(Cliente, pk=pk)
            cliente.alterado_em = timezone.now()
            cliente.alterado_por = request.user.id
            cliente.foto = body.get('foto', None)
            cliente.nome = body.get('nome', None)
            cliente.genero = body.get('genero', None)
            cliente.sobrenome = body.get('sobrenome', None)
            cliente.cpf = body.get('cpf', None)
            cliente.email = body.get('email', None)
            cliente.telefone_1 = body.get('telefone_1', None)
            cliente.telefone_2 = body.get('telefone_2', None)
            cliente.inadimplente = body.get('inadimplente', None)
            if body.get('endereco__endereco', None):
                endereco = Endereco()
                if body.get('endereco__id', None):
                    endereco = get_object_or_404(
                        Endereco, pk=body.get('endereco__id', None))
                    endereco.alterado_em = timezone.now()
                    endereco.alterado_por = request.user.id
                else:
                    endereco.criado_em = timezone.now()
                    endereco.criado_por = request.user.id
                cliente.endereco = endereco
                endereco.endereco = body.get('endereco__endereco', None)
                endereco.numero = body.get('endereco__numero', None)
                endereco.complemento = body.get('endereco__complemento', None)
                endereco.bairro = body.get('endereco__bairro', None)
                endereco.municipio = body.get('endereco__municipio', None)
                endereco.estado = body.get('endereco__estado', None)
                endereco.cep = body.get('endereco__cep', None)
                endereco.save()
            cliente.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def cliente_delete(request, pk):
    try:
        cliente = get_object_or_404(Cliente, pk=pk)
        cliente.delete()
        return JsonResponse({'status': True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
