from commons.models import Base64
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
from veterinaria.models import Medicamento

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def medicamentos_findall(request):
    filtro = request.GET.get('filtro', None)

    medicamentos = Medicamento.objects

    if filtro:
        medicamentos = medicamentos.filter(
            Q(medicamento__icontains=filtro)
            | Q(quantidade__icontains=filtro)
            | Q(unidade_medida__icontains=filtro)
        )

    medicamentos = medicamentos.all().values('id', 'medicamento', 'quantidade', 'unidade_medida', 'bula__id', 'bula__arquivo_base64', 'bula__extensao', 'anexo__id', 'anexo__arquivo_base64', 'anexo__extensao', 'observacao')

    if medicamentos:
        medicamentos = list(medicamentos)
    else:
        medicamentos = ()

    return JsonResponse({'data':medicamentos}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def medicamento_get(request, pk):
    try:
        medicamento = Medicamento.objects.filter(pk=pk).all().values('id', 'medicamento', 'quantidade', 'unidade_medida', 'bula__arquivo_base64', 'bula__extensao', 'anexo__arquivo_base64', 'anexo__extensao', 'observacao')
        if not medicamento:
            raise Http404('Medicamento não encontrado.')
        return JsonResponse(medicamento[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def medicamento_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            medicamento = Medicamento()
            medicamento.criado_por = request.user.id
            medicamento.criado_em = timezone.now()
            medicamento.medicamento = body.get('medicamento', None)
            medicamento.quantidade = body.get('quantidade', None)
            medicamento.unidade_medida = body.get('unidade_medida', None)
            if body.get('bula__base64', None):
                medicamento.bula = get_object_or_404(Base64, pk=body.get('bula__base64', None))
            if body.get('anexo__base64', None):
                medicamento.anexo = get_object_or_404(Base64, pk=body.get('anexo__base64', None))
            medicamento.observacao = body.get('observacao', None)
            medicamento.save()
            return JsonResponse({'status':True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def medicamento_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            medicamento = get_object_or_404(Medicamento, pk=pk)
            medicamento.alterado_em = timezone.now()
            medicamento.alterado_por = request.user.id
            medicamento.medicamento = body.get('medicamento', None)
            medicamento.quantidade = body.get('quantidade', None)
            medicamento.unidade_medida = body.get('unidade_medida', None)
            if body.get('bula__base64', None):
                medicamento.bula = get_object_or_404(Base64, pk=body.get('bula__base64', None))
            if body.get('anexo__base64', None):
                medicamento.anexo = get_object_or_404(Base64, pk=body.get('anexo__base64', None))
            medicamento.observacao = body.get('observacao', None)
            medicamento.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def medicamento_delete(request, pk):
    try:
        medicamento = get_object_or_404(Medicamento, pk=pk)
        medicamento.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
