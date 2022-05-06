from commons.models import Animal, Base64
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
from veterinaria.models import Exame

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def exames_findall(request):
    filtro = request.GET.get('filtro', None)

    exames = Exame.objects

    if filtro:
        exames = exames.filter(
            Q(animal__rga__icontains=filtro)
            | Q(animal__nome__icontains=filtro)
            | Q(descricao__icontains=filtro)
        )

    exames = exames.all().values('id', 'descricao', 'anexo__arquivo_base64', 'anexo__extensao', 'observacao', 'data_pedido', 'animal__id', 'animal__rga', 'animal__nome')

    if exames:
        exames = list(exames)
    else:
        exames = ()

    return JsonResponse({'data':exames}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def exame_get(request, pk):
    try:
        exame = Exame.objects.filter(pk=pk).all().values('id', 'descricao', 'anexo__arquivo_base64', 'anexo__extensao', 'observacao', 'data_pedido', 'animal__id', 'animal__rga', 'animal__nome')
        if not exame:
            raise Http404('Exame não encontrado.')
        return JsonResponse(exame[0], safe=False)
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def exame_create(request):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            exame = Exame()
            exame.criado_por = request.user.id
            exame.criado_em = timezone.now()
            exame.animal = get_object_or_404(Animal, pk=body.get('animal__id', None))
            if body.get('anexo__base64', None):
                exame.anexo = get_object_or_404(Base64, pk=body.get('anexo__base64', None))
            exame.data_pedido = body.get('data_pedido', None)
            exame.descricao = body.get('descricao', None)
            exame.observacao = body.get('observacao', None)
            exame.save()
            return JsonResponse({'status':True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def exame_edit(request, pk):
    body = request.body.decode('utf-8')
    if body:
        try:
            body = json.loads(body)
            exame = get_object_or_404(Exame, pk=pk)
            exame.alterado_em = timezone.now()
            exame.alterado_por = request.user.id
            exame.animal = get_object_or_404(Animal, pk=body.get('animal__id', None))
            if body.get('anexo__base64', None):
                exame.anexo = get_object_or_404(Base64, pk=body.get('anexo__base64', None))
            exame.data_pedido = body.get('data_pedido', None)
            exame.descricao = body.get('descricao', None)
            exame.observacao = body.get('observacao', None)
            exame.save()
            return JsonResponse({'status': True}, safe=False)
        except (KeyError, Exception) as ex:
            return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
    return HttpResponseBadRequest("O corpo da requisição está vazio!")


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def exame_delete(request, pk):
    try:
        exame = get_object_or_404(Exame, pk=pk)
        exame.delete()
        return JsonResponse({'status':True})
    except Exception as ex:
        return HttpResponseBadRequest("Ocorreu um erro ao efetuar a requisição! {}".format(ex))
