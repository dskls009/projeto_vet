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
from veterinaria.models import Doenca, Medicamento, Receituario

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def receitas_findall(request):
    filtro = request.GET.get('filtro', None)

    receitas = Receituario.objects

    if filtro:
        receitas = receitas.filter(
            Q(doenca__doenca__icontains=filtro)
            | Q(receita__icontains=filtro)
            | Q(medicamento__medicamento__icontains=filtro)
        )

    receitas = receitas.all().values('id', 'receita', 'anexo__arquivo_base64', 'anexo__extensao', 'observacao', 'medicamento__id', 'medicamento__medicamento', 'doenca__id', 'doenca__doenca')

    if receitas:
        receitas = list(receitas)
    else:
        receitas = ()

    return JsonResponse({'data':receitas}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def receita_get(request, pk):
    try:
        receita = Receituario.objects.filter(pk=pk).all().values('id', 'receita', 'anexo__arquivo_base64', 'anexo__extensao', 'observacao', 'medicamento__id', 'medicamento__medicamento', 'doenca__id', 'doenca__doenca')
        if not receita:
            raise Http404('Receita não encontrada.')
        return JsonResponse(receita[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def receita_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            receita = Receituario()
            receita.criado_por = request.user.id
            receita.criado_em = timezone.now()
            receita.doenca = get_object_or_404(Doenca, pk=body.get('doenca__id', None))
            receita.medicamento = get_object_or_404(Medicamento, pk=body.get('medicamento__id', None))
            if body.get('anexo__base64', None):
                receita.anexo = get_object_or_404(Base64, pk=body.get('anexo__base64', None))
            receita.receita = body.get('receita', None)
            receita.cronica = body.get('cronica', None)
            receita.observacao = body.get('observacao', None)
            receita.save()
            return JsonResponse({'status':True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def receita_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            receita = get_object_or_404(Receituario, pk=pk)
            receita.alterado_em = timezone.now()
            receita.alterado_por = request.user.id
            receita.doenca = get_object_or_404(Doenca, pk=body.get('doenca__id', None))
            receita.medicamento = get_object_or_404(Medicamento, pk=body.get('medicamento__id', None))
            if body.get('anexo__base64', None):
                receita.anexo = get_object_or_404(Base64, pk=body.get('anexo__base64', None))
            receita.receita = body.get('receita', None)
            receita.cronica = body.get('cronica', None)
            receita.observacao = body.get('observacao', None)
            receita.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def receita_delete(request, pk):
    try:
        receita = get_object_or_404(Receituario, pk=pk)
        receita.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
