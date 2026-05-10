from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

#  Colaborador 
class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    cargo = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

#  Cadastro de Equipamentos 
class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ca_numero = models.CharField(max_length=50, verbose_name="Número do CA") # Certificado de Aprovação

    def __str__(self):
        return self.nome

#  Controle de EPI 
class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('emprestado', 'Emprestado'),
        ('fornecido', 'Fornecido'),
        ('devolvido', 'Devolvido'),
        ('danificado', 'Danificado'),
        ('perdido', 'Perdido'),
    ]

    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)  
    data_entrega = models.DateTimeField(default=timezone.now) 
    data_prevista_devolucao = models.DateTimeField() 
    data_efetiva_devolucao = models.DateTimeField(blank=True, null=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='emprestado') 
    observacao_devolucao = models.TextField(blank=True, null=True) 

    #  Validação da Data Prevista 
    def clean(self):
        if self.data_prevista_devolucao and self.data_prevista_devolucao <= timezone.now():
            raise ValidationError('A data prevista para devolução deve ser posterior à data atual.')

    def __str__(self):
        return f"{self.colaborador.nome} - {self.equipamento.nome}"