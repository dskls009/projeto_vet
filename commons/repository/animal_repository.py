from commons.models import Cartao_Vacinacao, Cliente
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
from veterinaria.models import Animal

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def animais_findall(request):
    filtro = request.GET.get('filtro', None)
    tutor = request.GET.get('cliente', None)

    animais = Animal.objects

    if tutor:
        animais = animais.filter(cliente__id=tutor)

    if filtro:
        animais = animais.filter(
            Q(nome__icontains=filtro)
            | Q(especie__icontains=filtro)
            | Q(raca__icontains=filtro)
            | Q(rga__icontains=filtro)
            | Q(cor__icontains=filtro)
            | Q(cliente__cpf__icontains=filtro)
        )
    if filtro and filtro.lower() == 'castrado':
        animais = animais.filter(castrado=True)

    animais = animais.all().values('id', 'cliente__cpf', 'rga', 'nome', 'sexo', 'data_castracao', 'especie', 'raca', 'cor', 'nascimento', 'peso', 'porte', 'castrado')

    if animais:
        animais = list(animais)
    else:
        animais = ()

    return JsonResponse({'data':animais}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def animal_get(request, pk):
    try:
        animal = Animal.objects.filter(pk=pk).all().values('id', 'cliente__id', 'cliente__cpf', 'cartao_vacinacao__id', 'cartao_vacinacao__descricao', 'cartao_vacinacao__observacao', 'rga', 'nome', 'sexo', 'data_castracao', 'especie', 'raca', 'cor', 'nascimento', 'peso', 'porte', 'castrado')
        if not animal:
            raise Http404('Animal não encontrado.')
        return JsonResponse(animal[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def animal_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            animal = Animal()
            animal.criado_por = request.user.id
            animal.criado_em = timezone.now()
            animal.cliente = get_object_or_404(Cliente, pk=body.get('cliente__id', None))
            animal.nome = body.get('nome', None)
            animal.rga = body.get('rga', None)
            animal.foto = body.get('foto', None)
            animal.sexo = body.get('sexo', None)
            cartao_vacinacao = Cartao_Vacinacao()
            animal.cartao_vacinacao = cartao_vacinacao
            cartao_vacinacao.criado_em = timezone.now()
            cartao_vacinacao.criado_por = request.user.id
            if body.get('cartao_vacinacao__descricao', None):
                cartao_vacinacao.descricao = body.get('cartao_vacinacao__descricao', None)
            else:
                cartao_vacinacao.descricao = 'Cartão de '+animal.nome
            cartao_vacinacao.observacao = body.get('cartao_vacinacao__observacao', None)
            animal.especie = body.get('especie', None)
            animal.raca = body.get('raca', None)
            animal.cor = body.get('cor', None)
            animal.nascimento = body.get('nascimento', None)
            animal.data_castracao = body.get('data_castracao', None)
            animal.peso = body.get('peso', None)
            animal.porte = body.get('porte', None)
            animal.castrado = body.get('castrado', None)
            cartao_vacinacao.save()
            animal.save()
            return JsonResponse({'status':True, 'animal__id':animal.id}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def animal_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            animal = get_object_or_404(Animal, pk=pk)
            animal.alterado_em = timezone.now()
            animal.alterado_por = request.user.id
            animal.cliente = get_object_or_404(Cliente, pk=body.get('cliente__id', None))
            animal.nome = body.get('nome', None)
            animal.rga = body.get('rga', None)
            animal.foto = body.get('foto', None)
            animal.sexo = body.get('sexo', None)
            if body.get('cartao_vacinacao__id', None):
                cartao_vacinacao = get_object_or_404(Cartao_Vacinacao, pk=body.get('cartao_vacinacao__id', None))
                cartao_vacinacao.alterado_em = timezone.now()
                cartao_vacinacao.alterado_por = request.user.id
            else:
                cartao_vacinacao = Cartao_Vacinacao()
                cartao_vacinacao.criado_em = timezone.now()
                cartao_vacinacao.criado_por = request.user.id
            animal.cartao_vacinacao = cartao_vacinacao
            if body.get('cartao_vacinacao__descricao', None):
                cartao_vacinacao.descricao = body.get('cartao_vacinacao__descricao', None)
            else:
                cartao_vacinacao.descricao = 'Cartão de Vacinação'
            cartao_vacinacao.observacao = body.get('cartao_vacinacao__observacao', None)
            animal.especie = body.get('especie', None)
            animal.raca = body.get('raca', None)
            animal.cor = body.get('cor', None)
            animal.nascimento = body.get('nascimento', None)
            animal.data_castracao = body.get('data_castracao', None)
            animal.peso = body.get('peso', None)
            animal.porte = body.get('porte', None)
            animal.castrado = body.get('castrado', None)
            cartao_vacinacao.save()
            animal.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def animal_delete(request, pk):
    try:
        animal = get_object_or_404(Animal, pk=pk)
        animal.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
