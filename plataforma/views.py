from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Evento
from .forms import EventoForm
from django.core.files import File
import os
from io import BytesIO
from docx import Document  # Biblioteca para manipular arquivos DOCX (Word)

class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'index.html'
    success_url = reverse_lazy('sucesso')  # Substitua se necessário

    def gerar_contrato(self, contrato_padrao, nome, cpf, email, endereco_residencial, endereco_evento, data, hora):
        """Preenche o contrato padrão com os dados do evento preservando o estilo"""
        if contrato_padrao and contrato_padrao.endswith('.docx'):
            # Abre o arquivo DOCX padrão
            doc = Document(contrato_padrao)

            # Substitui as variáveis no contrato pelos dados do evento
            for p in doc.paragraphs:
                for run in p.runs:  # Preserva o estilo de cada parte do parágrafo
                    run.text = run.text.replace('{{nome}}', nome)
                    run.text = run.text.replace('{{cpf}}', cpf)  # Corrigido de {{cpf_ed}} para {{cpf}}
                    run.text = run.text.replace('{{email}}', email)
                    run.text = run.text.replace('{{endereco}}', endereco_residencial)
                    run.text = run.text.replace('{{endereco_evento}}', endereco_evento)
                    run.text = run.text.replace('{{data}}', data.strftime('%d/%m/%Y'))
                    run.text = run.text.replace('{{hora}}', hora.strftime('%H:%M'))

            # Define o nome do arquivo gerado
            contrato_nome = f"{nome.replace(' ', '_')}_{endereco_evento.replace(' ', '_')}.docx"

            # Salva o arquivo gerado no diretório contratos_gerados
            caminho_gerado = os.path.join('contratos_gerados', contrato_nome)
            doc.save(caminho_gerado)

            return caminho_gerado  # Retorna o caminho do arquivo gerado

    def form_valid(self, form):
        # Obtém os dados do formulário
        nome = form.cleaned_data.get('nome_completo')
        email = form.cleaned_data.get('email')
        cpf = form.cleaned_data.get('cpf')
        endereco_evento = form.cleaned_data.get('endereco_evento')
        endereco_residencial = form.cleaned_data.get('endereco_residencial')
        data = form.cleaned_data.get('data')
        hora = form.cleaned_data.get('hora')

        # Caminho do contrato padrão
        contrato_padrao = os.path.join('contratos_padroes', '17-08-24_Cha_de_Fraldas_Maycon_Costa.docx')

        # Gera o contrato preenchido e obtém o caminho do arquivo gerado
        contrato_gerado = self.gerar_contrato(
            contrato_padrao, nome, cpf, email, endereco_residencial, endereco_evento, data, hora
        )

        # Salva o caminho do arquivo na sessão para ser usado na próxima requisição
        self.request.session['contrato_gerado'] = contrato_gerado

        # Continua para a página de sucesso
        return redirect('sucesso')


def download_contrato(request):
    contrato_gerado = request.session.get('contrato_gerado')

    if not contrato_gerado or not os.path.exists(contrato_gerado):
        return HttpResponse("Contrato não encontrado.", status=404)

    with open(contrato_gerado, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(contrato_gerado)}"'
        return response


def sucesso(request):
    return render(request, 'sucesso.html')
