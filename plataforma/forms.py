from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    BOMBA_OPCOES = [
        ('bomba_eletrica', 'Bomba Elétrica'),
        ('profissional', 'Profissional'),
    ]

    bomba_opcao = forms.ChoiceField(
        choices=BOMBA_OPCOES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Escolha uma opção",
    )

    class Meta:
        model = Evento
        fields = [
            'nome_completo',
            'cpf',
            'email',
            'endereco_residencial',
            'endereco_evento',
            'tipo_evento',
            'chopp_quantidade_marca',
            'bomba_opcao',
            'data',
            'hora',
            'valor_total',
            'forma_pagamento',
            'observacoes',
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco_residencial': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco_evento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_evento': forms.TextInput(attrs={'class': 'form-control'}),
            'chopp_quantidade_marca': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'valor_total': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'nome_completo': 'Nome Completo',
            'cpf': 'CPF',
            'email': 'E-mail',
            'endereco_residencial': 'Endereço Residencial',
            'endereco_evento': 'Endereço do Evento',
            'tipo_evento': 'Tipo de Evento',
            'chopp_quantidade_marca': 'Chopp (Quantidade e Marca)',
            'bomba_opcao': 'Escolha uma opção',
            'data': 'Data',
            'hora': 'Hora',
            'valor_total': 'Valor Total',
            'forma_pagamento': 'Forma de Pagamento',
            'observacoes': 'Observações',
        }
