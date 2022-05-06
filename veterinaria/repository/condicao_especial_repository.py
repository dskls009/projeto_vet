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
from veterinaria.models import Condicao_Especial
from commons.models import Animal

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def condicoes_especiais_findall(request):
    filtro = request.GET.get('filtro', None)
    animal = request.GET.get('animal', None)

    condicoes_especiais = Condicao_Especial.objects

    if animal:
        condicoes_especiais = condicoes_especiais.filter(animal__id=animal)

    if filtro:
        condicoes_especiais = condicoes_especiais.filter(
            Q(descricao__icontains=filtro)
            | Q(aquisicao__icontains=filtro)
            | Q(cura__icontains=filtro)
            | Q(observacao__icontains=filtro)
        )

    if filtro and (filtro.lower() == 'cronica' or filtro.lower() == 'crônica'):
        condicoes_especiais = condicoes_especiais.filter(cronica=True)

    condicoes_especiais = condicoes_especiais.all().values('id', 'descricao', 'cronica', 'aquisicao', 'cura', 'observacao')

    if condicoes_especiais:
        condicoes_especiais = list(condicoes_especiais)
    else:
        condicoes_especiais = ()

    if not animal:
        condicoes_especiais = ()

    return JsonResponse({'data':condicoes_especiais}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def condicao_especial_get(request, pk):
    try:
        condicao_especial = Condicao_Especial.objects.filter(pk=pk).all().values('id', 'descricao', 'cronica', 'aquisicao', 'cura', 'observacao')
        if not condicao_especial:
            raise Http404('Condição Especial não encontrada.')
        return JsonResponse(condicao_especial[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def condicao_especial_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            condicao_especial = Condicao_Especial()
            condicao_especial.criado_por = request.user.id
            condicao_especial.criado_em = timezone.now()
            condicao_especial.animal = get_object_or_404(Animal, pk=body.get('animal__id', None))
            condicao_especial.descricao = body.get('descricao', None)
            condicao_especial.cronica = body.get('cronica', None)
            condicao_especial.aquisicao = body.get('aquisicao', None)
            condicao_especial.cura = body.get('cura', None)
            condicao_especial.observacao = body.get('observacao', None)
            condicao_especial.save()
            return JsonResponse({'status':True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def condicao_especial_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            condicao_especial = get_object_or_404(Condicao_Especial, pk=pk)
            condicao_especial.alterado_em = timezone.now()
            condicao_especial.alterado_por = request.user.id
            condicao_especial.animal = get_object_or_404(Animal, pk=body.get('animal__id', None))
            condicao_especial.descricao = body.get('descricao', None)
            condicao_especial.cronica = body.get('cronica', None)
            condicao_especial.aquisicao = body.get('aquisicao', None)
            condicao_especial.cura = body.get('cura', None)
            condicao_especial.observacao = body.get('observacao', None)
            condicao_especial.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def condicao_especial_delete(request, pk):
    try:
        condicao_especial = get_object_or_404(Condicao_Especial, pk=pk)
        condicao_especial.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
