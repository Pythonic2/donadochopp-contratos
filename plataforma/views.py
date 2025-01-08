from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
# from .models import , ContratoAssinado
from .forms import EventoForm,EventoProdutoForm
from docx import Document
import os
import subprocess
from .models import *
from django.urls import reverse


def home(request):

    return render(request,'index.html')

def get_cliente(request):
    if request.method == 'GET':
        pesquisa = request.GET.get('termo')
        if pesquisa:  # Verifica se há uma pesquisa para realizar
            clientes = Cliente.objects.filter(nome_completo__icontains=pesquisa)
        else:
            clientes = None
    return render(request,'parciais/clientes.html',{'clientes':clientes})




# def converter_para_pdf(caminho_docx):
#     """Converte um arquivo .docx para .pdf usando LibreOffice"""
#     caminho_pdf = caminho_docx.replace('.docx', '.pdf')
#     try:
#         subprocess.run(
#             ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(caminho_docx), caminho_docx],
#             check=True
#         )
#         return caminho_pdf if os.path.exists(caminho_pdf) else None
#     except subprocess.CalledProcessError as e:
#         print(f"Erro ao converter para PDF: {e}")
#         return None


class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'criar_evento.html'

    def dispatch(self, request, *args, **kwargs):
        # Armazena o id_cliente da URL
        self.id_cliente = kwargs.get('id_cliente')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Obtém o cliente com base no id_cliente
        cliente = get_object_or_404(Cliente, id=self.id_cliente)

        # Associa o cliente e o usuário logado ao evento
        form.instance.cliente = cliente
        form.instance.usuario = self.request.user

        # Salva o evento e captura a instância salva
        evento = form.save()

        # Redireciona para a view de AddProduto, passando o id_evento
        return redirect(reverse('add-produto', kwargs={'id_evento': evento.id}))
    

class AddProduto(CreateView):
    model = EventoProduto
    form_class = EventoProdutoForm
    template_name = 'cadastrar_produtos.html'

    def dispatch(self, request, *args, **kwargs):
        self.id_evento = kwargs.get('id_evento')  # Obtém o ID do evento da URL
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['id_evento'] = self.id_evento  # Passa o ID do evento para o formulário
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_evento'] = self.id_evento  # Adiciona o id_evento no contexto
        return context

    def form_valid(self, form):
        # Associa o evento automaticamente no backend
        evento = get_object_or_404(Evento, id=self.id_evento)
        form.instance.evento = evento

        # Salva o formulário e redireciona para a mesma página
        form.save()
        return redirect(reverse('add-produto', kwargs={'id_evento': self.id_evento}))

import os
from docx import Document

def gerar_contrato(contrato_padrao, cliente, evento, produtos):
    """
    Preenche o contrato padrão com os dados do evento e do cliente,
    cria uma pasta com o CPF do cliente e salva o contrato dentro dela.
    """
    if contrato_padrao and contrato_padrao.endswith('.docx'):
        # Abre o arquivo DOCX padrão
        doc = Document(contrato_padrao)

        # Substitui as variáveis do cliente e do evento
        for p in doc.paragraphs:
            for run in p.runs:  # Preserva o estilo de cada parte do parágrafo
                run.text = run.text.replace('{{nome}}', cliente.nome_completo or "")
                run.text = run.text.replace('{{cpf_ed}}', cliente.cpf or "")
                run.text = run.text.replace('{{email}}', cliente.email or "")
                run.text = run.text.replace('{{endereco}}', cliente.endereco_residencial or "")
                run.text = run.text.replace('{{endereco_evento}}', evento.endereco_evento or "")
                run.text = run.text.replace('{{data}}', evento.data.strftime('%d/%m/%Y') if evento.data else "")
                run.text = run.text.replace('{{hora}}', evento.hora.strftime('%H:%M') if evento.hora else "")
                run.text = run.text.replace('{{choppeira}}', 'Chopeira a Bomba' if evento.bomba_opcao == 'choppeira_bomba' else "Chopeira Elétrica")
                run.text = run.text.replace('{{prof}}', 'e 01 (um) profissional' if evento.profissional else "")

                # Substitui os produtos contratados
                if produtos.exists():  # Verifica se existem produtos
                    if len(produtos) == 1:  # Apenas um produto
                        descricao_produtos = f"{produtos[0].produto.nome} ({produtos[0].quantidade} unidade)"
                    else:  # Vários produtos
                        descricao_produtos = ", ".join(
                            [f"{produto.produto.nome} ({produto.quantidade} unidades)" for produto in produtos]
                        )
                else:
                    descricao_produtos = ""  # Nenhum produto

                run.text = run.text.replace('{{produtos}}', descricao_produtos)

        # Define o diretório do cliente com base no CPF
        diretorio_cliente = os.path.join('contratos_gerados', cliente.cpf)
        os.makedirs(diretorio_cliente, exist_ok=True)  # Cria o diretório, se não existir

        # Define o caminho completo do arquivo gerado
        contrato_nome = f"{cliente.nome_completo.replace(' ', '_')}_{evento.tipo_evento.replace(' ', '_')}.docx"
        caminho_docx = os.path.join(diretorio_cliente, contrato_nome)

        # Salva o arquivo .docx com as substituições
        doc.save(caminho_docx)

        return caminho_docx  # Retorna o caminho do arquivo .docx gerado

    raise Exception("Contrato padrão inválido ou não encontrado.")


def finalizar_contrato(request, id_evento):
    """
    Gera um contrato preenchido com os dados do evento, cliente e produtos.
    """
    # Obtém o evento
    evento = get_object_or_404(Evento, id=id_evento)

    # Obtém o cliente associado ao evento
    cliente = evento.cliente

    # Obtém os produtos relacionados ao evento
    produtos = EventoProduto.objects.filter(evento=evento)
    print(cliente.nome_completo)
    # Caminho do contrato padrão
    contrato_padrao = os.path.join('contratos_padroes', 'contrato_base.docx')

    # Gera o contrato preenchido
    contrato_gerado = gerar_contrato(
        contrato_padrao=contrato_padrao,
        cliente=cliente,
        evento=evento,
        produtos=produtos
    )

    # Certifique-se de que o arquivo gerado existe antes de salvar na sessão
    if not os.path.exists(contrato_gerado):
        return HttpResponse("Erro ao gerar o contrato.", status=500)

    # Salva o caminho do arquivo na sessão para ser usado na próxima requisição
    with open(contrato_gerado, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(contrato_gerado)}"'
        return response
    # Redireciona para a página de download
    return redirect('home')



