from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_colaboradores, name='listar_colaboradores'),
    path('novo/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('excluir/<int:id>/', views.excluir_colaborador, name='excluir_colaborador'),
]