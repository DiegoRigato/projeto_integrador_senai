from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError
from .models import Colaborador, Equipamento, Emprestimo

@login_required
def listagem_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    filtro_nome = request.GET.get('colaborador')
    
    if filtro_nome:
        colaboradores = colaboradores.filter(nome__icontains=filtro_nome)
        
    return render(request, 'colaboradores/listagem_colaboradores.html', {'colaboradores': colaboradores})

@login_required
def novo_colaborador(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        try:
            colaborador = Colaborador(nome=nome)
            colaborador.save()
            messages.success(request, "Colaborador cadastrado com sucesso!")
            return redirect('novo_colaborador')
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar: {e}")
            return redirect('novo_colaborador')
            
    return render(request, 'colaboradores/cadastro_colaborador.html')

@login_required
def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    if request.method == "POST":
        colaborador.nome = request.POST.get('nome')
        colaborador.save()
        messages.success(request, "Colaborador updated successfully!")
        return redirect('listagem_colaboradores')
    return render(request, 'colaboradores/editar_colaborador.html', {'colaborador': colaborador})

@login_required
def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.delete()
    messages.success(request, "Colaborador excluído com sucesso!")
    return redirect('listagem_colaboradores')

@login_required
def listagem_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    return render(request, 'colaboradores/listagem_equipamentos.html', {'equipamentos': equipamentos})

@login_required
def novo_equipamento(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        
        if Equipamento.objects.filter(nome__iexact=nome.strip()).exists():
            messages.error(request, f"Falha no cadastro: O equipamento '{nome}' já está cadastrado no sistema.")
            return redirect('novo_equipamento')

        try:
            equipamento = Equipamento(nome=nome.strip())
            equipamento.save()
            messages.success(request, "Equipamento cadastrado com sucesso!")
            return redirect('novo_equipamento')
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar: {e}")
            return redirect('novo_equipamento')
            
    return render(request, 'colaboradores/cadastro_equipamento.html')
@login_required
def excluir_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    try:
        equipamento.delete()
        messages.success(request, "Equipamento excluído com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao excluir equipamento: {e}")
        
    return redirect('listagem_equipamentos')

@login_required
def novo_emprestimo(request):
    if request.method == "POST":
        colaborador_id = request.POST.get('colaborador')
        equipamento_id = request.POST.get('equipamento')
        data_entrega_str = request.POST.get('data_entrega')
        data_prevista_str = request.POST.get('data_prevista')
        status = request.POST.get('status')

        if status == 'emprestado':
            ja_possui_emprestimo = Emprestimo.objects.filter(
                colaborador_id=colaborador_id,
                equipamento_id=equipamento_id,
                status='emprestado'
            ).exists()
            
            if ja_possui_emprestimo:
                messages.error(request, "Aviso: Este colaborador já possui um empréstimo ATIVO para este mesmo tipo de equipamento e não devolveu ainda.")
                return redirect('novo_emprestimo')

        data_entrega = parse_datetime(data_entrega_str)
        if not data_entrega:
            data_entrega = timezone.now()

        if data_entrega and timezone.is_naive(data_entrega):
            data_entrega = make_aware(data_entrega)

        if status == 'fornecido':
            data_prevista = data_entrega
        else:
            data_prevista = parse_datetime(data_prevista_str)
            if data_prevista and timezone.is_naive(data_prevista):
                data_prevista = make_aware(data_prevista)

        if status == 'emprestado' and data_entrega and data_prevista:
            if data_prevista < data_entrega:
                messages.error(request, "Falha no cadastro: A data prevista para devolução deve ser posterior à data de entrega.")
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
    return render(request, 'colaboradores/emprestimo_equipamento.html', context)
@login_required
def relatorio_emprestimos(request):
    emprestimos = Emprestimo.objects.all()

    filtro_colaborador = request.GET.get('colaborador')
    filtro_equipamento = request.GET.get('equipamento')
    filtro_status = request.GET.get('status')

    if filtro_colaborador:
        emprestimos = emprestimos.filter(colaborador__nome__icontains=filtro_colaborador)
        
    if filtro_equipamento:
        emprestimos = emprestimos.filter(equipamento__nome__icontains=filtro_equipamento)
        
    if filtro_status:
        emprestimos = emprestimos.filter(status=filtro_status)

    context = {
        'emprestimos': emprestimos
    }
    return render(request, 'colaboradores/relatorio_emprestimos.html', context)

@login_required
def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)
    
    if request.method == "POST":
        novo_status = request.POST.get('status')
        emprestimo.status = novo_status
        
        # Se for devolvido, danificado ou perdido, exige a data de baixa e o motivo
        if novo_status in ['devolvido', 'danificado', 'perdido']:
            data_efetiva_str = request.POST.get('data_efetiva')
            if data_efetiva_str:
                data_efetiva = parse_datetime(data_efetiva_str)
                if data_efetiva and timezone.is_naive(data_efetiva):
                    emprestimo.data_efetiva_devolucao = make_aware(data_efetiva)
                else:
                    emprestimo.data_efetiva_devolucao = data_efetiva
            
            # Captura o motivo digitado pelo usuário
            emprestimo.observacao_devolucao = request.POST.get('observacao')
        else:
            # Se voltar para emprestado ou fornecido, limpa os campos de baixa
            emprestimo.data_efetiva_devolucao = None
            emprestimo.observacao_devolucao = ""
            
        try:
            emprestimo.save()
            messages.success(request, "Status do empréstimo atualizado com sucesso!")
            return redirect('relatorio_emprestimos')
        except Exception as e:
            messages.error(request, f"Erro ao atualizar status: {e}")
            return redirect('relatorio_emprestimos')

    data_efetiva_formatada = ""
    if emprestimo.data_efetiva_devolucao:
        data_efetiva_formatada = emprestimo.data_efetiva_devolucao.strftime('%Y-%m-%dT%H:%M')

    context = {
        'emprestimo': emprestimo,
        'data_efetiva_formatada': data_efetiva_formatada
    }
    return render(request, 'colaboradores/editar_emprestimo.html', context)