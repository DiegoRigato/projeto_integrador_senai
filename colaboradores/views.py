from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Colaborador, Equipamento, Emprestimo
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

def home(request):
    return render(request, 'colaboradores/home.html')

# GERENCIAMENTO DE COLABORADORES 

def listar_colaboradores(request):
    nome_pesquisa = request.GET.get('nome')
    if nome_pesquisa:
        colaboradores = Colaborador.objects.filter(nome__icontains=nome_pesquisa)
    else:
        colaboradores = Colaborador.objects.all()
     
    return render(request, 'colaboradores/listagem.html', {'colaboradores': colaboradores})

def cadastrar_colaborador(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        cargo = request.POST.get('cargo')
        setor = request.POST.get('setor')
        try:
            Colaborador.objects.create(nome=nome, cpf=cpf, cargo=cargo, setor=setor)
            messages.success(request, "Colaborador cadastrado com sucesso!")
            return redirect('listagem_colaboradores')
        except Exception:
            messages.error(request, "Erro ao cadastrar colaborador.")
    
    
    return render(request, 'colaboradores/cadastro.html')

def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == "POST":
        colaborador.nome = request.POST.get('nome')
        colaborador.cpf = request.POST.get('cpf')
        colaborador.cargo = request.POST.get('cargo')
        colaborador.setor = request.POST.get('setor')
        colaborador.save()
        messages.success(request, "Dados atualizados com sucesso!")
        return redirect('listagem_colaboradores')
        
    return render(request, 'colaboradores/editar_colaborador.html', {'colaborador': colaborador})

def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.delete()
    messages.success(request, "Colaborador excluído com sucesso!")
    return redirect('listagem_colaboradores')


#  GERENCIAMENTO DE EQUIPAMENTOS (EPIs) 

def cadastro_equipamento(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        ca = request.POST.get('ca_numero')
        descricao = request.POST.get('descricao')
        try:
            
            Equipamento.objects.create(nome=nome, ca_numero=ca, descricao=descricao)
            messages.success(request, "Equipamento (EPI) cadastrado com sucesso!")
            return redirect('listagem_equipamentos')
        except Exception:
            messages.error(request, "Erro ao cadastrar equipamento.")

   
    return render(request, 'colaboradores/cadastro_equipamento.html')

def listagem_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    return render(request, 'colaboradores/listagem_equipamentos.html', {'equipamentos': equipamentos})

def excluir_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    try:
        equipamento.delete()
        messages.success(request, "Equipamento removido com sucesso!")
    except Exception:
        messages.error(request, "Erro ao excluir: este equipamento pode estar vinculado a um empréstimo.")
    
    return redirect('listagem_equipamentos')


# CONTROLE DE EMPRÉSTIMOS 

def novo_emprestimo(request):
    if request.method == "POST":
        colaborador_id = request.POST.get('colaborador')
        equipamento_id = request.POST.get('equipamento')
        data_entrega_str = request.POST.get('data_entrega')
        data_prevista_str = request.POST.get('data_prevista')
        status = request.POST.get('status')

        data_entrega = parse_datetime(data_entrega_str)
        if not data_entrega:
            data_entrega = timezone.now()

        if data_entrega and timezone.is_naive(data_entrega):
            data_entrega = make_aware(data_entrega)

        #  Se for fornecido, a previsão assume a mesma data da entrega
        if status == 'fornecido':
            data_prevista = data_entrega
        else:
            data_prevista = parse_datetime(data_prevista_str)
            if data_prevista and timezone.is_naive(data_prevista):
                data_prevista = make_aware(data_prevista)

        if status == 'emprestado' and data_entrega and data_prevista:
            if data_prevista < data_entrega:
                messages.error(request, "Falha no cadastro: A data prevista para devolução deve ser posterior à data de entrega do empréstimo.")
                return redirect('novo_emprestimo')

        try:
            colaborador = Colaborador.objects.get(id=colaborador_id)
            equipamento = Equipamento.objects.get(id=equipamento_id)

            emprestimo = Emprestimo(
                colaborador=colaborador,
                equipamento=equipamento,
                data_entrega=data_entrega,
                data_prevista_devolucao=data_prevista,
                status=status
            )
            
            emprestimo.full_clean()
            emprestimo.save()
            
            messages.success(request, "Empréstimo registrado com sucesso!")
            return redirect('relatorio_emprestimos')
            
        except ValidationError as e:
            if hasattr(e, 'message_dict') and 'data_prevista_devolucao' in e.message_dict:
                messages.error(request, f"Falha no cadastro: {e.message_dict['data_prevista_devolucao'][0]}")
            else:
                messages.error(request, f"Falha no cadastro: {e.messages[0]}")
            return redirect('novo_emprestimo')
        except Exception as e:
            messages.error(request, f"Erro inesperado ao salvar: {e}")
            return redirect('novo_emprestimo')

    context = {
        'colaboradores': Colaborador.objects.all(),
        'equipamentos': Equipamento.objects.all(),
    }
    return render(request, 'colaboradores/emprestimo.html', context)


# 2. TELA DE ATUALIZAÇÃO DE STATUS 
def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)
    
    if request.method == "POST":
        novo_status = request.POST.get('status')
        emprestimo.status = novo_status
        
        if novo_status in ['devolvido', 'danificado', 'perdido']:
            data_efetiva_str = request.POST.get('data_efetiva')
            if data_efetiva_str:
                data_efetiva = parse_datetime(data_efetiva_str)
                # Garante que a data tem fuso horário antes de salvar no banco
                if data_efetiva and timezone.is_naive(data_efetiva):
                    emprestimo.data_efetiva_devolucao = make_aware(data_efetiva)
                else:
                    emprestimo.data_efetiva_devolucao = data_efetiva
            
            emprestimo.observacao_devolucao = request.POST.get('observacao')
        else:
            # Se voltou para Emprestado ou Fornecido, limpa os campos de baixa
            emprestimo.data_efetiva_devolucao = None
            emprestimo.observacao_devolucao = ""
            
        try:
            emprestimo.save()
            messages.success(request, "Status do empréstimo atualizado com sucesso!")
            return redirect('relatorio_emprestimos')
        except Exception as e:
            messages.error(request, f"Erro ao atualizar status: {e}")
            return redirect('relatorio_emprestimos')

    # Formata a data para o HTML conseguir ler caso ela já exista no banco
    data_efetiva_formatada = ""
    if emprestimo.data_efetiva_devolucao:
        data_efetiva_formatada = emprestimo.data_efetiva_devolucao.strftime('%Y-%m-%dT%H:%M')

    context = {
        'emprestimo': emprestimo,
        'data_efetiva_formatada': data_efetiva_formatada
    }
    return render(request, 'colaboradores/editar_emprestimo.html', context)

# 3. TELA DE RELATÓRIOS E HISTÓRICO 

def relatorio_emprestimos(request):
    # Começa pegando todos os empréstimos do banco de dados
    emprestimos = Emprestimo.objects.all()
    
    # Captura o que o usuário digitou 
    filtro_colaborador = request.GET.get('colaborador')
    filtro_equipamento = request.GET.get('equipamento')
    filtro_status = request.GET.get('status')
    
    # Aplica os filtros um após o outro 
    if filtro_colaborador:
        emprestimos = emprestimos.filter(colaborador__nome__icontains=filtro_colaborador)
        
    if filtro_equipamento:
        emprestimos = emprestimos.filter(equipamento__nome__icontains=filtro_equipamento)
        
    if filtro_status:
        emprestimos = emprestimos.filter(status=filtro_status)
        
    # Retorna a página com a lista filtrada
    return render(request, 'colaboradores/relatorio_emprestimos.html', {'emprestimos': emprestimos})