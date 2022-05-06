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
from veterinaria.models import Atendimento, Cirurgia, Consulta, Emergencia, Medicamento, Medicamento_Administrado


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def medicamentos_administrados_findall(request):
    filtro = request.GET.get('filtro', None)
    consulta = request.GET.get('consulta', None)
    cirurgia = request.GET.get('cirurgia', None)
    emergencia = request.GET.get('emergencia', None)
    atendimento = request.GET.get('atendimento', None)

    medicamentos_administrados = Medicamento_Administrado.objects

    if consulta:
        medicamentos_administrados = medicamentos_administrados.filter(
            consulta__id=consulta)
    elif cirurgia:
        medicamentos_administrados = medicamentos_administrados.filter(
            cirurgia__id=cirurgia)
    elif emergencia:
        medicamentos_administrados = medicamentos_administrados.filter(
            emergencia__id=emergencia)
    elif atendimento:
        medicamentos_administrados = medicamentos_administrados.filter(
            atendimento__id=atendimento)


    if filtro:
        medicamentos_administrados = medicamentos_administrados.filter(
            Q(medicamento__medicamento__icontains=filtro)
            | Q(quantidade_administrada__icontains=filtro)
        )

    medicamentos_administrados = medicamentos_administrados.all().values('id',
                                                                         'medicamento__id',
                                                                         'medicamento__medicamento',
                                                                         'medicamento__unidade_medida',
                                                                         'consulta__id',
                                                                         'consulta__descricao',
                                                                         'cirurgia__id',
                                                                         'cirurgia__descricao',
                                                                         'emergencia__id',
                                                                         'emergencia__descricao',
                                                                         'atendimento__id',
                                                                         'atendimento__descricao',
                                                                         'quantidade_administrada',
                                                                         'data_aplicacao',
                                                                         'observacao')

    if medicamentos_administrados:
        medicamentos_administrados = list(medicamentos_administrados)
    else:
        medicamentos_administrados = ()

    return JsonResponse({'data': medicamentos_administrados}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def medicamento_administrado_get(request, pk):
    try:
        medicamento_administrado = Medicamento_Administrado.objects.filter(pk=pk).all().values('id',
                                                                                               'medicamento__id',
                                                                                               'medicamento__medicamento',
                                                                                               'medicamento__unidade_medida',
                                                                                               'consulta__id',
                                                                                               'consulta__descricao',
                                                                                               'cirurgia__id',
                                                                                               'cirurgia__descricao',
                                                                                               'emergencia__id',
                                                                                               'emergencia__descricao',
                                                                                               'atendimento__id',
                                                                                               'atendimento__descricao',
                                                                                               'quantidade_administrada',
                                                                                               'data_aplicacao',
                                                                                               'observacao')
        if not medicamento_administrado:
            raise Http404('Medicamento Administrado não encontrado.')
        return JsonResponse(medicamento_administrado[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def medicamento_administrado_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            medicamento_administrado = Medicamento_Administrado()
            medicamento_administrado.criado_por = request.user.id
            medicamento_administrado.criado_em = timezone.now()
            medicamento_administrado.medicamento = get_object_or_404(
                Medicamento, pk=body.get('medicamento__id', None))
            if body.get('consulta__id', None):
                medicamento_administrado.consulta = get_object_or_404(
                    Consulta, pk=body.get('consulta__id', None))
            if body.get('cirurgia__id', None):
                medicamento_administrado.cirurgia = get_object_or_404(
                    Cirurgia, pk=body.get('cirurgia__id', None))
            if body.get('emergencia__id', None):
                medicamento_administrado.emergencia = get_object_or_404(
                    Emergencia, pk=body.get('emergencia__id', None))
            if body.get('etendimento__id', None):
                medicamento_administrado.atendimento = get_object_or_404(
                    Atendimento, pk=body.get('atendimento__id', None))
            medicamento_administrado.quantidade_administrada = body.get(
                'quantidade_administrada', None)
            medicamento_administrado.data_aplicacao = body.get(
                'data_aplicacao', None)
            medicamento_administrado.observacao = body.get('observacao', None)
            medicamento_administrado.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def medicamento_administrado_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            medicamento_administrado = get_object_or_404(
                Medicamento_Administrado, pk=pk)
            medicamento_administrado.alterado_em = timezone.now()
            medicamento_administrado.alterado_por = request.user.id
            medicamento_administrado.medicamento = get_object_or_404(
                Medicamento, pk=body.get('medicamento__id', None))
            medicamento_administrado.consulta = get_object_or_404(
                Consulta, pk=body.get('consulta__id', None))
            medicamento_administrado.cirurgia = get_object_or_404(
                Cirurgia, pk=body.get('cirurgia__id', None))
            medicamento_administrado.emergencia = get_object_or_404(
                Emergencia, pk=body.get('emergencia__id', None))
            medicamento_administrado.atendimento = get_object_or_404(
                Atendimento, pk=body.get('atendimento__id', None))
            medicamento_administrado.quantidade_administrada = body.get(
                'quantidade_administrada', None)
            medicamento_administrado.data_aplicacao = body.get(
                'data_aplicacao', None)
            medicamento_administrado.observacao = body.get('observacao', None)
            medicamento_administrado.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def medicamento_administrado_delete(request, pk):
    try:
        medicamento_administrado = get_object_or_404(
            Medicamento_Administrado, pk=pk)
        medicamento_administrado.delete()
        return JsonResponse({'status': True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
