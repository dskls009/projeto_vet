from django.shortcuts import get_object_or_404
from django.utils import timezone  # pega data e hora com fuso horário
from django.http import HttpResponseBadRequest, JsonResponse, Http404, HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q, base
import json
import pandas as pd
import base64
import os
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from commons.models import Base64


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def base64_findall(request):
    filtro = request.GET.get('filtro', None)

    base64 = Base64.objects

    if filtro:
        base64 = base64.filter(
            Q(extensao__icontains=filtro)
        )

    base64 = base64.all().values('id', 'arquivo_base64', 'extensao')

    if base64:
        base64 = list(base64)
    else:
        base64 = ()

    return JsonResponse({'data': base64}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def base64_download(request, pk):
    try:
        _base64 = Base64.objects.filter(pk=pk).all().values('id', 'arquivo_base64', 'extensao')
        nome = _base64[0].get('extensao')
        arquivo = _base64[0].get('arquivo_base64').partition('base64,')[2]
        datatype = _base64[0].get('arquivo_base64').partition('base64,')[0]
        datatype = datatype[5:-1]
        binario = base64.b64decode(arquivo)
        if not _base64:
            raise Http404('Base64 não encontrado.')
        response = HttpResponse(binario, content_type=datatype)
        response['Content-Disposition'] = 'attachment; filename="%s"'%nome
        return response
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def base64_get(request, pk):
    try:
        base64 = Base64.objects.filter(pk=pk).all().values('id', 'arquivo_base64', 'extensao')
        if not base64:
            raise Http404('Base64 não encontrado.')
        return JsonResponse(base64[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def base64_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            if Base64.objects.filter(arquivo_base64=body.get('base64', None)).first():
                base64 = Base64.objects.filter(arquivo_base64=body.get('base64', None)).first()
            else:
                base64 = Base64()
                base64.criado_por = request.user.id
                base64.criado_em = timezone.now()
            base64.arquivo_base64 = body.get('base64', None)
            base64.extensao = body.get('extensao', None)
            base64.save()
            return JsonResponse({'status': True, 'base64__id': base64.id}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def base64_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            base64 = get_object_or_404(Base64, pk=pk)
            base64.alterado_em = timezone.now()
            base64.alterado_por = request.user.id
            base64.arquivo_base64 = body.get('base64', None)
            base64.extensao = body.get('extensao', None)
            base64.save()
            return JsonResponse({'status': True, 'base64__id': base64.id}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def base64_delete(request, pk):
    try:
        base64 = get_object_or_404(Base64, pk=pk)
        base64.delete()
        return JsonResponse({'status': True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
