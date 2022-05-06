import os
from commons.models import Animal, Cliente
from django.shortcuts import get_object_or_404
from django.utils import timezone  # pega data e hora com fuso horário
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
import json
import pandas
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def clientes_relatorio(request):
    nome = request.GET.get('nome', None)
    sobrenome = request.GET.get('sobrenome', None)
    cpf = request.GET.get('cpf', None)
    email = request.GET.get('email', None)
    telefone = request.GET.get('telefone', None)
    inadimplente = request.GET.get('inadimplente', None)
    genero = request.GET.get('genero', None)
    col_id = request.GET.get('col_id', None)
    col_cpf = request.GET.get('col_cpf', None)
    col_nome = request.GET.get('col_nome', None)
    col_sobrenome = request.GET.get('col_sobrenome', None)
    col_genero = request.GET.get('col_genero', None)
    col_email = request.GET.get('col_email', None)
    col_telefone_1 = request.GET.get('col_telefone_1', None)
    col_telefone_2 = request.GET.get('col_telefone_2', None)
    col_inadimplente = request.GET.get('col_inadimplente', None)
    export = request.GET.get('export', None)

    relatorio = Cliente.objects

    colunas = list()

    if col_id:
        colunas.append(col_id)
    if col_cpf:
        colunas.append(col_cpf)
    if col_nome:
        colunas.append(col_nome)
    if col_sobrenome:
        colunas.append(col_sobrenome)
    if col_genero:
        colunas.append(col_genero)
    if col_email:
        colunas.append(col_email)
    if col_telefone_1:
        colunas.append(col_telefone_1)
    if col_telefone_2:
        colunas.append(col_telefone_2)
    if col_inadimplente:
        colunas.append(col_inadimplente)

    if nome:
        relatorio = relatorio.filter(
            Q(nome__icontains=nome)
        )
    
    if sobrenome:
        relatorio = relatorio.filter(
            Q(sobrenome__icontains=sobrenome)
        )

    if cpf:
        relatorio = relatorio.filter(
            Q(cpf__icontains=cpf)
        )
    
    if email:
        relatorio = relatorio.filter(
            Q(email__icontains=email)
        )

    if telefone:
        relatorio = relatorio.filter(
            Q(telefone_1__icontains=telefone)
            | Q(telefone_2__icontains=telefone)
        )

    if inadimplente and inadimplente.lower() == 'true':
        relatorio = relatorio.filter(
            Q(inadimplente=True)
        )
    elif inadimplente and inadimplente.lower() == 'false':
        relatorio = relatorio.filter(
            Q(inadimplente=False)
        )

    if genero:
        relatorio = relatorio.filter(
            Q(genero__icontains=genero)
        )

    if colunas:
        relatorio = relatorio.all().values(*colunas)
    else:
        relatorio = relatorio.all().values('id', 'cpf', 'nome', 'sobrenome', 'genero', 'email', 'telefone_1', 'telefone_2', 'inadimplente')

    if relatorio:
        relatorio = list(relatorio)
    else:
        relatorio = ()

    if export and export == 'true':
        # df = pandas.DataFrame(relatorio)
        # writer = pandas.ExcelWriter('Clientes.xlsx', engine='xlsxwriter')
        # df.to_excel(writer, sheet_name='Clientes', startrow=2)
        # book = writer.book
        # sheet = writer.sheets['Clientes']
        # bold = book.add_format({'bold': True})
        # sheet.write('A2', 'Relatório de Clientes', bold)
        # writer.save()
        template = get_template('report_cliente.html')
        context = {
            'relatorio': relatorio,
            'colunas': colunas
        }
        html  = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    return JsonResponse({'data':relatorio}, safe=False)


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def animais_relatorio(request):
    cliente__nome = request.GET.get('cliente__nome', None)
    cliente__sobrenome = request.GET.get('cliente__sobrenome', None)
    cliente__cpf = request.GET.get('cliente__cpf', None)
    cliente__inadimplente = request.GET.get('cliente__inadimplente', None)
    rga = request.GET.get('rga', None)
    nome = request.GET.get('nome', None)
    especie = request.GET.get('especie', None)
    raca = request.GET.get('raca', None)
    cor = request.GET.get('cor', None)
    peso = request.GET.get('peso', None)
    porte = request.GET.get('porte', None)
    castrado = request.GET.get('castrado', None)
    data_castracao_de = request.GET.get('data_castracao_de', None)
    data_castracao_ate = request.GET.get('data_castracao_ate', None)
    sexo = request.GET.get('sexo', None)
    col_id = request.GET.get('col_id', None)
    col_cliente__cpf = request.GET.get('col_cliente__cpf', None)
    col_cliente__nome = request.GET.get('col_cliente__nome', None)
    col_cliente__sobrenome = request.GET.get('col_cliente__sobrenome', None)
    col_cliente__inadimplente = request.GET.get('col_cliente__inadimplente', None)
    col_rga = request.GET.get('col_rga', None)
    col_nome = request.GET.get('col_nome', None)
    col_especie = request.GET.get('col_especie', None)
    col_raca = request.GET.get('col_raca', None)
    col_cor = request.GET.get('col_cor', None)
    col_peso = request.GET.get('col_peso', None)
    col_porte = request.GET.get('col_porte', None)
    col_sexo = request.GET.get('col_sexo', None)
    col_castrado = request.GET.get('col_castrado', None)
    col_data_castracao = request.GET.get('col_data_castracao', None)
    export = request.GET.get('export', None)

    relatorio = Animal.objects

    colunas = list()

    if col_id:
        colunas.append(col_id)
    if col_cliente__cpf:
        colunas.append(col_cliente__cpf)
    if col_cliente__nome:
        colunas.append(col_cliente__nome)
    if col_cliente__sobrenome:
        colunas.append(col_cliente__sobrenome)
    if col_cliente__inadimplente:
        colunas.append(col_cliente__inadimplente)
    if col_rga:
        colunas.append(col_rga)
    if col_nome:
        colunas.append(col_nome)
    if col_especie:
        colunas.append(col_especie)
    if col_raca:
        colunas.append(col_raca)
    if col_cor:
        colunas.append(col_cor)
    if col_peso:
        colunas.append(col_peso)
    if col_porte:
        colunas.append(col_porte)
    if col_sexo:
        colunas.append(col_sexo)
    if col_castrado:
        colunas.append(col_castrado)
    if col_data_castracao:
        colunas.append(col_data_castracao)


    if rga:
        relatorio = relatorio.filter(
            Q(rga__icontains=rga)
        )

    if nome:
        relatorio = relatorio.filter(
            Q(nome__icontains=nome)
        )

    if especie:
        relatorio = relatorio.filter(
            Q(especie__icontains=especie)
        )

    if raca:
        relatorio = relatorio.filter(
            Q(raca__icontains=raca)
        )

    if cor:
        relatorio = relatorio.filter(
            Q(cor__icontains=cor)
        )

    if peso:
        relatorio = relatorio.filter(
            Q(peso__icontains=peso)
        )

    if porte:
        relatorio = relatorio.filter(
            Q(porte__icontains=porte)
        )

    if castrado and castrado.lower() == 'true':
        relatorio = relatorio.filter(
            Q(castrado=True)
        )
    elif castrado and castrado.lower() == 'false':
        relatorio = relatorio.filter(
            Q(castrado=False)
        )

    if sexo:
        relatorio = relatorio.filter(
            Q(sexo__icontains=sexo)
        )

    if data_castracao_de or data_castracao_ate:
        relatorio = relatorio.filter(
            Q(data_castracao__range=(data_castracao_de, data_castracao_ate))
        )

    if cliente__nome:
        relatorio = relatorio.filter(
            Q(cliente__nome__icontains=cliente__nome)
        )
    
    if cliente__sobrenome:
        relatorio = relatorio.filter(
            Q(cliente__sobrenome__icontains=cliente__sobrenome)
        )

    if cliente__cpf:
        relatorio = relatorio.filter(
            Q(cliente__cpf__icontains=cliente__cpf)
        )

    if cliente__inadimplente and cliente__inadimplente.lower() == 'true':
        relatorio = relatorio.filter(
            Q(cliente__inadimplente=True)
        )
    elif cliente__inadimplente and cliente__inadimplente.lower() == 'false':
        relatorio = relatorio.filter(
            Q(cliente__inadimplente=False)
        )

    if colunas:
        relatorio = relatorio.all().values(*colunas)
    else:
        relatorio = relatorio.all().values('id', 'cliente__cpf', 'cliente__nome', 'cliente__sobrenome', 'cliente__inadimplente', 'rga', 'nome', 'especie', 'raca', 'cor', 'peso', 'porte', 'castrado', 'data_castracao', 'sexo')

    if relatorio:
        relatorio = list(relatorio)
    else:
        relatorio = ()

    if export and export == 'true':
        df = pandas.DataFrame(relatorio)
        writer = pandas.ExcelWriter('Animais.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Animais', startrow=2)
        book = writer.book
        sheet = writer.sheets['Animais']
        bold = book.add_format({'bold': True})
        sheet.write('A2', 'Relatório de Animais', bold)
        writer.save()

    return JsonResponse({'data':relatorio}, safe=False)
