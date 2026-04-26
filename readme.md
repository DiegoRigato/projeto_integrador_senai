# Sistema de Gerenciamento de EPIs - Indústria Têxtil

Este sistema foi desenvolvido para melhorar o controle e uso de Equipamentos de Proteção Individual (EPIs).

## Funcionalidades (Etapa 2)
* Cadastro de colaboradores com feedback visual (Bootstrap).
* Listagem de colaboradores com persistência em banco de dados.
* Busca funcional por nome.
* Exclusão segura com modal de confirmação.

## Como Executar o Projeto
1. Instale as dependências: `pip install -r requirements.txt`
2. Prepare o banco de dados: `python manage.py migrate`
3. Inicie o servidor: `python manage.py runserver`
4. Acesse: `http://127.0.0.1:8000/colaboradores/`