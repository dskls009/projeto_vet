from django.db import models

class Base64(models.Model):
    arquivo_base64 = models.TextField()
    extensao = models.CharField(max_length=250)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Endereco(models.Model):
    endereco = models.CharField(max_length=320)
    numero = models.PositiveIntegerField(null=True)
    complemento = models.CharField(max_length=320, null=True)
    bairro = models.CharField(max_length=320, null=True)
    municipio = models.CharField(max_length=320, null=True)
    estado = models.CharField(max_length=320, null=True)
    cep = models.CharField(max_length=320, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Usuario(models.Model):
    crmv = models.CharField(max_length=50, unique=True, null=True)
    foto = models.ImageField(null=True)
    nome = models.CharField(max_length=250)
    sobrenome = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    telefone_1 = models.CharField(max_length=250, null=True)
    telefone_2 = models.CharField(max_length=250, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
    usuario = models.CharField(max_length=250)
    senha = models.CharField(max_length=250)
    username = property(usuario)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

    def get_username(self):
        return self.usuario

    def __str__(self):
        return self.usuario

    def save(self, *args, **kwargs):
        super(Usuario, self).save()
        from django.contrib.auth.models import User
        if self.id:
            user = User.objects.filter(pk=self.id).first()
            if not user:
                user = User(id=self.pk)
            user.username = self.usuario
            user.password = self.senha
            user.save()

class Cliente(models.Model):
    foto = models.ImageField(null=True)
    cpf = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=250)
    sobrenome = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    telefone_1 = models.CharField(max_length=250, null=True)
    telefone_2 = models.CharField(max_length=250, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
    inadimplente = models.BooleanField(default=False)
    genero = models.CharField(max_length=250, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.nome

class Cartao_Vacinacao(models.Model):
    descricao = models.CharField(max_length=250)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Animal(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    foto = models.ImageField(null=True)
    rga = models.CharField(max_length=250, unique=True)
    nome = models.CharField(max_length=250)
    especie = models.CharField(max_length=250, null=True)
    raca = models.CharField(max_length=250, null=True)
    cor = models.CharField(max_length=250, null=True)
    nascimento = models.DateField(null=True)
    peso = models.FloatField(null=True)
    porte = models.CharField(max_length=250, null=True)
    castrado = models.BooleanField(default=False)
    data_castracao = models.DateField(null=True)
    sexo = models.CharField(max_length=250, null=True)
    cartao_vacinacao = models.ForeignKey(Cartao_Vacinacao, on_delete=models.CASCADE, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.nome

class Album(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    data = models.DateField(null=True)
    observacao = models.TextField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)

class Foto(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    foto = models.ImageField()
    data = models.DateField(null=True)
    legenda = models.CharField(max_length=250, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    criado_por = models.CharField(max_length=250, null=True)
    alterado_por = models.CharField(max_length=250, null=True)
