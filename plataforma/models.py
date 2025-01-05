from django.db import models
from django.core.files import File
import os
from io import BytesIO
from docx import Document  # Biblioteca para manipular arquivos DOCX (Word)

class Evento(models.Model):
    BOMBA_OPCOES = [
        ('bomba_eletrica', 'Bomba Elétrica'),
        ('profissional', 'Profissional'),
    ]

    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    endereco_residencial = models.CharField(max_length=255)
    endereco_evento = models.CharField(max_length=255)
    tipo_evento = models.CharField(max_length=50)
    chopp_quantidade_marca = models.CharField(max_length=255, help_text="Informe a quantidade e marca do chopp.")
    bomba_opcao = models.CharField(
        max_length=20,
        choices=BOMBA_OPCOES,
        null=True,
        blank=True,
        verbose_name="Escolha uma opção"
    )
    data = models.DateField()
    hora = models.TimeField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    forma_pagamento = models.CharField(max_length=50, choices=[
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto')
    ], default='dinheiro')
    observacoes = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return f"{self.tipo_evento} - {self.data} {self.hora} - {self.nome_completo}"


class ContratoPadrao(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Contrato")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição do Contrato")
    arquivo = models.FileField(upload_to='contratos_padroes/', verbose_name="Arquivo do Contrato Padrão")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.nome
