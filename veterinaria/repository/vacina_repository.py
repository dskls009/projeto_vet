from commons.models import Animal, Cartao_Vacinacao
from django.shortcuts import get_object_or_404
from django.utils import timezone  # pega data e hora com fuso horário
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q, OuterRef, Subquery
import json
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from veterinaria.models import Consulta, Vacina

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def vacinas_findall(request):
    filtro = request.GET.get('filtro', None)

    vacinas = Vacina.objects

    if filtro:
        vacinas = vacinas.filter(
            Q(vacina__icontains=filtro)
            | Q(cartao_vacinacao__descricao__icontains=filtro)
        )

    vacinas = vacinas.all().values('id', 'cartao_vacinacao__id', 'cartao_vacinacao__descricao', 'vacina', 'dose', 'data_aplicacao', 'proxima_dose', 'observacao')

    if vacinas:
        vacinas = list(vacinas)
    else:
        vacinas = ()
    
    return JsonResponse({'data':vacinas}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def vacina_get(request, pk):
    try:
        vacina = Vacina.objects.filter(pk=pk).all().values('id', 'cartao_vacinacao__id', 'cartao_vacinacao__descricao', 'vacina', 'dose', 'data_aplicacao', 'proxima_dose', 'observacao')
        if not vacina:
            raise Http404('Vacina não encontrada.')
        return JsonResponse(vacina[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def vacina_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            vacina = Vacina()
            vacina.criado_por = request.user.id
            vacina.criado_em = timezone.now()
            animal = get_object_or_404(Animal, pk=body.get('animal__id', None))
            cartao_vacinacao = get_object_or_404(Cartao_Vacinacao, pk=animal.cartao_vacinacao.id)
            vacina.cartao_vacinacao = cartao_vacinacao
            vacina.vacina = body.get('vacina', None)
            vacina.dose = body.get('dose', None)
            vacina.data_aplicacao = body.get('data_aplicacao', None)
            vacina.proxima_dose = body.get('proxima_dose', None)
            vacina.observacao = body.get('observacao', None)
            vacina.save()
            return JsonResponse({'status':True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def vacina_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            vacina = get_object_or_404(Vacina, pk=pk)
            vacina.alterado_em = timezone.now()
            vacina.alterado_por = request.user.id
            animal = get_object_or_404(Animal, pk=body.get('animal__id', None))
            cartao_vacinacao = get_object_or_404(Cartao_Vacinacao, pk=animal.cartao_vacinacao.id)
            vacina.cartao_vacinacao = cartao_vacinacao
            vacina.vacina = body.get('vacina', None)
            vacina.dose = body.get('dose', None)
            vacina.data_aplicacao = body.get('data_aplicacao', None)
            vacina.proxima_dose = body.get('proxima_dose', None)
            vacina.observacao = body.get('observacao', None)
            vacina.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def vacina_delete(request, pk):
    try:
        vacina = get_object_or_404(Vacina, pk=pk)
        vacina.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
