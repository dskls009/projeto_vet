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
from veterinaria.models import Doenca

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def doencas_findall(request):
    filtro = request.GET.get('filtro', None)

    doencas = Doenca.objects

    if filtro:
        doencas = doencas.filter(
            Q(doenca__icontains=filtro)
        )

    if filtro and (filtro.lower() == 'cronica' or filtro.lower() == 'crônica'):
        doencas = doencas.filter(cronica=True)

    doencas = doencas.all().values('id', 'doenca', 'cronica', 'observacao')

    if doencas:
        doencas = list(doencas)
    else:
        doencas = ()

    return JsonResponse({'data':doencas}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def doenca_get(request, pk):
    try:
        doenca = Doenca.objects.filter(pk=pk).all().values('id', 'doenca', 'cronica', 'observacao')
        if not doenca:
            raise Http404('Doença não encontrada.')
        return JsonResponse(doenca[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def doenca_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            doenca = Doenca()
            doenca.criado_por = request.user.id
            doenca.criado_em = timezone.now()
            doenca.doenca = body.get('doenca', None)
            doenca.cronica = body.get('cronica', None)
            doenca.observacao = body.get('observacao', None)
            doenca.save()
            return JsonResponse({'status':True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def doenca_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            doenca = get_object_or_404(Doenca, pk=pk)
            doenca.alterado_em = timezone.now()
            doenca.alterado_por = request.user.id
            doenca.doenca = body.get('doenca', None)
            doenca.cronica = body.get('cronica', None)
            doenca.observacao = body.get('observacao', None)
            doenca.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def doenca_delete(request, pk):
    try:
        doenca = get_object_or_404(Doenca, pk=pk)
        doenca.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
