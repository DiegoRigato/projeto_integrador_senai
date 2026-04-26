from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Colaborador

def listar_colaboradores(request):
    nome_busca = request.GET.get('nome')
    if nome_busca:
        colaboradores = Colaborador.objects.filter(nome__icontains=nome_busca)
    else:
        colaboradores = Colaborador.objects.all()
    return render(request, 'colaboradores/listagem.html', {'colaboradores': colaboradores})

def cadastrar_colaborador(request):
    if request.method == "POST":
        try:
            Colaborador.objects.create(
                nome=request.POST.get('nome'),
                cpf=request.POST.get('cpf'),
                cargo=request.POST.get('cargo'),
                setor=request.POST.get('setor')
            )
            messages.success(request, 'Colaborador cadastrado com sucesso!') # Requisito 38
        except:
            messages.error(request, 'Erro ao cadastrar. Verifique os dados.')
        return redirect('cadastrar_colaborador') # Requisito 39
    return render(request, 'colaboradores/cadastro.html')

def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.delete()
    messages.warning(request, 'Colaborador removido.')
    return redirect('listar_colaboradores')