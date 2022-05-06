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
from veterinaria.models import Atendimento
from commons.models import Animal

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def atendimentos_findall(request):
    filtro = request.GET.get('filtro', None)
    animal = request.GET.get('animal', None)

    atendimentos = Atendimento.objects

    if animal:
        atendimentos = atendimentos.filter(animal__id=animal)

    if filtro:
        atendimentos = atendimentos.filter(
            Q(descricao__icontains=filtro)
            | Q(animal__cliente__cpf__icontains=filtro)
            | Q(animal__nome__icontains=filtro)
            | Q(animal__rga__icontains=filtro)
            | Q(datahora_inicio__icontains=filtro)
            | Q(datahora_fim__icontains=filtro)
        )

    atendimentos = atendimentos.all().values('id', 'animal__id', 'animal__rga', 'animal__nome', 'animal__cliente__cpf', 'descricao', 'datahora_inicio', 'datahora_fim', 'observacao')

    if atendimentos:
        atendimentos = list(atendimentos)
    else:
        atendimentos = ()

    return JsonResponse({'data':atendimentos}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def atendimento_get(request, pk):
    try:
        atendimento = Atendimento.objects.filter(pk=pk).all().values('id', 'animal__id', 'animal__rga', 'animal__nome', 'animal__cliente__cpf', 'descricao', 'datahora_inicio', 'datahora_fim', 'observacao')
        if not atendimento:
            raise Http404('Atendimento não encontrado.')
        return JsonResponse(atendimento[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def atendimento_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            atendimento = Atendimento()
            atendimento.criado_por = request.user.id
            atendimento.criado_em = timezone.now()
            atendimento.animal = get_object_or_404(Animal, pk=body.get('animal__id', None))
            atendimento.descricao = body.get('descricao', None)
            if body.get('data_inicio', None):
                if body.get('hora_inicio', None) == '':
                    datahora_inicio = body.get('data_inicio', None)+' 00:00'
                else:
                    datahora_inicio = body.get('data_inicio', None)+' '+body.get('hora_inicio', None)
            else:
                datahora_inicio = timezone.now()
            if body.get('data_fim', None):
                if body.get('hora_fim', None) == '':
                    datahora_fim = body.get('data_fim', None)+' 00:00'
                else:
                    datahora_fim = body.get('data_fim', None)+' '+body.get('hora_fim', None)
            else:
                datahora_fim = timezone.now()
            atendimento.datahora_inicio = datahora_inicio
            atendimento.datahora_fim = datahora_fim
            atendimento.observacao = body.get('observacao', None)
            atendimento.save()
            return JsonResponse({'status':True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def atendimento_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            atendimento = get_object_or_404(Atendimento, pk=pk)
            atendimento.alterado_em = timezone.now()
            atendimento.alterado_por = request.user.id
            atendimento.animal = get_object_or_404(Animal, pk=body.get('animal__id', None))
            atendimento.descricao = body.get('descricao', None)
            if body.get('data_inicio', None):
                if body.get('hora_inicio', None) == '':
                    datahora_inicio = body.get('data_inicio', None)+' 00:00'
                else:
                    datahora_inicio = body.get('data_inicio', None)+' '+body.get('hora_inicio', None)
            else:
                datahora_inicio = timezone.now()
            if body.get('data_fim', None):
                if body.get('hora_fim', None) == '':
                    datahora_fim = body.get('data_fim', None)+' 00:00'
                else:
                    datahora_fim = body.get('data_fim', None)+' '+body.get('hora_fim', None)
            else:
                datahora_fim = timezone.now()
            atendimento.datahora_inicio = datahora_inicio
            atendimento.datahora_fim = datahora_fim
            atendimento.observacao = body.get('observacao', None)
            atendimento.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def atendimento_delete(request, pk):
    try:
        atendimento = get_object_or_404(Atendimento, pk=pk)
        atendimento.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
