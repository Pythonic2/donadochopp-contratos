from django import forms
from .models import Evento, Cliente, EventoProduto,Produto


class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome do Produto",
                "class": "form-control",
                "maxlength": "100",
                "required": "true"
            }
        ),
        label="Nome do Produto"
    )
    disponivel = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"  # Classe Bootstrap para checkbox (opcional)
            }
        ),
        required=True,  # Define que o campo é obrigatório
        label="Disponível: ",  # Texto exibido ao lado do checkbox
        initial=True  # Define o valor inicial como marcado
    )

    valor = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Valor do Produto",
                "class": "form-control",
                "step": "0.01",
                "min": "0"
            }
        ),
        label="Valor",
        max_digits=10,
        decimal_places=2
    )
    litros = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Quantidade em Litros",
                "class": "form-control",
                "min": "0"
            }
        ),
        label="Litros",
        required=False
    )

    class Meta:
        model = Produto
        fields = ['nome', 'disponivel', 'valor', 'litros']



class ClienteForm(forms.ModelForm):
    nome_completo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome Completo",
                "class": "form-control",
                "maxlength": "100",
                "required": "true"
            }
        ),
        label="Nome Completo"
    )
    cpf = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "CPF (somente números)",
                "class": "form-control",
                "maxlength": "11",
                "required": "true"
            }
        ),
        label="CPF"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
                "required": "true"
            }
        ),
        label="Email"
    )
    endereco_residencial = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Endereço Residencial",
                "class": "form-control",
                "required": "true"
            }
        ),
        label="Endereço Residencial"
    )
    celular = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Celular (somente números)",
                "class": "form-control",
                "maxlength": "11",
                "required": "true"
            }
        ),
        label="Celular"
    )

    class Meta:
        model = Cliente
        fields = ['nome_completo', 'cpf', 'email', 'endereco_residencial', 'celular']


from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    endereco_evento = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Endereço do Evento",
                "class": "form-control"
            }
        )
    )
    tipo_evento = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tipo de Evento",
                "class": "form-control"
            }
        )
    )
    bomba_opcao = forms.ChoiceField(
        choices=Evento.BOMBA_OPCOES,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        ),
        required=True
    )
    profissional = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"  # Classe Bootstrap para checkbox (opcional)
            }
        ),
        required=True,  # Permite que o checkbox não seja obrigatório
        label="Contratar Profissional: ",  # Texto exibido ao lado do checkbox
    )
    data = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "Data do Evento",
                "class": "form-control",
                "type": "date"
            }
        )
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "placeholder": "Hora do Evento",
                "class": "form-control",
                "type": "time"
            }
        )
    )
    forma_pagamento = forms.ChoiceField(
        choices=Evento._meta.get_field('forma_pagamento').choices,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )
    observacoes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Observações",
                "class": "form-control",
                "rows": 3
            }
        ),
        required=False
    )

    class Meta:
        model = Evento
        fields = [
            'endereco_evento', 'tipo_evento', 'bomba_opcao','profissional', 
            'data', 'hora', 'forma_pagamento', 'observacoes'
        ]




class EventoProdutoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.none(),
        widget=forms.HiddenInput(),  # Campo oculto
        label="Evento"
    )
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Selecione um produto",
            }
        ),
        label="Produto"
    )
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": 1,
                "placeholder": "Quantidade"
            }
        ),
        label="Quantidade",
        min_value=1
    )

    class Meta:
        model = EventoProduto
        fields = ['evento', 'produto', 'quantidade']

    def __init__(self, *args, **kwargs):
        id_evento = kwargs.pop('id_evento', None)  # Obtém o ID do evento do backend
        super().__init__(*args, **kwargs)
        if id_evento:
            self.fields['evento'].queryset = Evento.objects.filter(id=id_evento)
            self.fields['evento'].initial = id_evento  # Pré-seleciona o evento
