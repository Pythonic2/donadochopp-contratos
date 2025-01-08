from django.db import models

class Cliente(models.Model):
    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=100)
    endereco_residencial = models.CharField(max_length=255)
    celular = models.CharField(max_length=11)

    def __str__(self):
        return self.nome_completo


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    disponivel = models.BooleanField(default=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    litros = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.nome} - {self.litros}L - R${self.valor} '


class Evento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="eventos")
    BOMBA_OPCOES = [
        ('choppeira_eletrica', 'Choppeira Elétrica'),
        ('choppeira_bomba', 'Choppeira Bomba'),
    ]

    endereco_evento = models.CharField(max_length=255)
    tipo_evento = models.CharField(max_length=50)
    produtos = models.ManyToManyField(Produto, through='EventoProduto', related_name='eventos')
    bomba_opcao = models.CharField(
        max_length=20,
        choices=BOMBA_OPCOES,
        null=True,
        blank=True,
        verbose_name="Escolha uma opção"
    )
    profissional = models.BooleanField(default=False)
    data = models.DateField()
    hora = models.TimeField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    forma_pagamento = models.CharField(max_length=50, choices=[
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto')
    ], default='dinheiro')
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_evento} - {self.data} {self.hora}"


class EventoProduto(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.evento} - {self.produto} ({self.quantidade})"
