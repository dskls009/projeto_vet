from django.db import models
from commons.models import Animal, Album, Base64, Cartao_Vacinacao


class Consulta(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    descricao = models.CharField(max_length=250)
    datahora_inicio = models.DateTimeField(null=True)
    datahora_fim = models.DateTimeField(null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Cirurgia(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    descricao = models.CharField(max_length=250)
    datahora_inicio = models.DateTimeField(null=True)
    datahora_fim = models.DateTimeField(null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Emergencia(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    descricao = models.CharField(max_length=250)
    datahora_inicio = models.DateTimeField(null=True)
    datahora_fim = models.DateTimeField(null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Atendimento(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    descricao = models.CharField(max_length=250)
    datahora_inicio = models.DateTimeField(null=True)
    datahora_fim = models.DateTimeField(null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Vacina(models.Model):
    cartao_vacinacao = models.ForeignKey(Cartao_Vacinacao, on_delete=models.CASCADE, null=False)
    vacina = models.CharField(max_length=250)
    dose = models.CharField(max_length=250, null=True)
    data_aplicacao = models.DateField(null=True)
    proxima_dose = models.DateField(null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Medicamento(models.Model):
    medicamento = models.CharField(max_length=250)
    quantidade = models.CharField(max_length=250, null=True)
    unidade_medida = models.CharField(max_length=250, null=True)
    bula = models.ForeignKey(Base64, on_delete=models.CASCADE, null=True, related_name='bula')
    anexo = models.ForeignKey(Base64, on_delete=models.CASCADE, null=True, related_name='anexo')
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Medicamento_Administrado(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, null=False)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null=True)
    cirurgia = models.ForeignKey(Cirurgia, on_delete=models.CASCADE, null=True)
    emergencia = models.ForeignKey(Emergencia, on_delete=models.CASCADE, null=True)
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE, null=True)
    quantidade_administrada = models.CharField(max_length=250, null=True)
    data_aplicacao = models.DateField(null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Condicao_Especial(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=False)
    descricao = models.CharField(max_length=250)
    cronica = models.BooleanField(default=False)
    aquisicao = models.DateField(null=True)
    cura = models.DateField(null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Doenca(models.Model):
    doenca = models.CharField(max_length=250)
    cronica = models.BooleanField(default=False)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Receituario(models.Model):
    receita = models.TextField(null=True)
    anexo = models.ForeignKey(Base64, on_delete=models.CASCADE, null=True)
    doenca = models.ForeignKey(Doenca, on_delete=models.CASCADE, null=False)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Exame(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=250)
    data_pedido = models.DateField(null=True)
    anexo = models.ForeignKey(Base64, on_delete=models.CASCADE, null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)
