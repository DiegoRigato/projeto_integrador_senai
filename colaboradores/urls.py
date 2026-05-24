from django.urls import path
from . import views

urlpatterns = [
    path('', views.listagem_colaboradores, name='listagem_colaboradores'),
    path('novo/', views.novo_colaborador, name='novo_colaborador'),
    path('editar/<int:id>/', views.editar_colaborador, name='editar_colaborador'),
    path('excluir/<int:id>/', views.excluir_colaborador, name='excluir_colaborador'),
    path('equipamentos/', views.listagem_equipamentos, name='listagem_equipamentos'),
    path('equipamentos/novo/', views.novo_equipamento, name='novo_equipamento'),
    path('novo-emprestimo/', views.novo_emprestimo, name='novo_emprestimo'),
    path('emprestimos/relatorio/', views.relatorio_emprestimos, name='relatorio_emprestimos'),
    path('emprestimos/editar/<int:id>/', views.editar_emprestimo, name='editar_emprestimo'),
    path('equipamentos/excluir/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),
]