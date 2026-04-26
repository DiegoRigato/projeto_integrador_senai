from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=150)
    cargo = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.nome
