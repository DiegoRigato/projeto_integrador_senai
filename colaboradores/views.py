from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Colaborador, Equipamento, Emprestimo

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
        data_entrega = request.POST.get('data_entrega')
        data_prevista = request.POST.get('data_prevista')
        status = request.POST.get('status')

       
        if data_prevista and data_entrega:
            if data_prevista < data_entrega:
                messages.error(request, "Erro: A data de devolução não pode ser anterior à data de entrega!")
                
                return redirect('novo_emprestimo')
      

        try:
            colaborador = Colaborador.objects.get(id=colaborador_id)
            equipamento = Equipamento.objects.get(id=equipamento_id)

            Emprestimo.objects.create(
                colaborador=colaborador,
                equipamento=equipamento,
                data_entrega=data_entrega,
                data_prevista_devolucao=data_prevista,
                status=status
            )
            messages.success(request, "Empréstimo registrado com sucesso!")
            return redirect('listagem_colaboradores')
        except Exception as e:
            messages.error(request, f"Erro ao registrar: {e}")

    colaboradores = Colaborador.objects.all()
    equipamentos = Equipamento.objects.all()
    
    context = {
        'colaboradores': colaboradores,
        'equipamentos': equipamentos,
        'hoje': timezone.now().strftime('%Y-%m-%dT%H:%M')
    }
    return render(request, 'colaboradores/emprestimo.html', context)