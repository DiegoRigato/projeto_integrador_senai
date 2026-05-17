from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('listagem/', views.listar_colaboradores, name='listagem_colaboradores'),
    path('novo/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('excluir/<int:id>/', views.excluir_colaborador, name='excluir_colaborador'),
    path('equipamentos/', views.listagem_equipamentos, name='listagem_equipamentos'),
    path('equipamentos/novo/', views.cadastro_equipamento, name='cadastro_equipamento'),
    path('emprestimos/novo/', views.novo_emprestimo, name='novo_emprestimo'),
    path('emprestimos/novo/', views.novo_emprestimo, name='novo_emprestimo'),
    path('colaboradores/editar/<int:id>/', views.editar_colaborador, name='editar_colaborador'),
    path('equipamentos/excluir/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),
    path('emprestimos/novo/', views.novo_emprestimo, name='novo_emprestimo'),
    path('emprestimos/relatorio/', views.relatorio_emprestimos, name='relatorio_emprestimos'),
    path('emprestimos/editar/<int:id>/', views.editar_emprestimo, name='editar_emprestimo'),
]