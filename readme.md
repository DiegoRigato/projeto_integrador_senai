# Protekta - Sistema de Gerenciamento e Auditoria de EPIs

O **Protekta** é uma aplicação web desenvolvida com Django e banco de dados MySQL, criada para automatizar, controlar e auditar o fluxo de fornecimento e empréstimo de Equipamentos de Proteção Individual (EPIs) em uma indústria do setor têxtil.

O sistema tem como objetivo reduzir riscos de acidentes, melhorar o controle de EPIs e garantir maior rastreabilidade das operações realizadas pelos colaboradores.

---

# Tecnologias Utilizadas

## Backend
- Python 3.x
- Django Framework 4.2

## Banco de Dados
- MySQL

## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

## Segurança
- Python-Dotenv

---

# Funcionalidades da Aplicação

## Gestão Completa de Colaboradores (CRUD)

### Cadastro
- Registro de novos colaboradores
- Permanência na mesma tela após criação

### Feedback Visual
- Mensagens de sucesso e erro utilizando componentes Bootstrap

### Listagem Inteligente
- Exibição de todos os colaboradores cadastrados
- Barra de pesquisa funcional por nome

### Atualização Segura
- Tela de edição preenchida automaticamente com os dados atuais

### Exclusão com Confirmação
- Confirmação antes da exclusão através de alertas/modais

---

## Controle de Fluxos e Regras de Negócio

### Diferenciação de Categorias

Separação automática entre:

- **Empréstimo**
  - Temporário
  - Possui data de devolução

- **Fornecimento**
  - Permanente
  - Sem necessidade de devolução

### Trava de Duplicidade Ativa

Impede o registro de empréstimos duplicados do mesmo EPI para o mesmo colaborador.

### Validação Cronológica

Bloqueia datas de devolução anteriores à data de entrega.

### Auditoria de Ocorrências

Quando um EPI é marcado como:

- Danificado
- Perdido

O sistema exige justificativa obrigatória e exibe o motivo em destaque no histórico.

---

# Boas Práticas e Segurança

## Variáveis de Ambiente (`.env`)

As credenciais do banco de dados são isoladas do código-fonte.

## `.gitignore`

Proteção contra envio de:
- Arquivos `.env`
- Cache do Python
- Arquivos temporários

## `requirements.txt`

Controle completo das dependências do projeto.

---

# Como Executar o Projeto

## 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

---

## 2. Criar e Ativar o Ambiente Virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_NAME=nome_do_banco
DB_USER=usuario_mysql
DB_PASSWORD=senha_mysql
DB_HOST=localhost
DB_PORT=3306
```

---

## 5. Executar as Migrações

```bash
python manage.py migrate
```

---

## 6. Criar um Superusuário

```bash
python manage.py createsuperuser
```

---

## 7. Iniciar o Servidor

```bash
python manage.py runserver
```

---

## 8. Acessar o Sistema

Abra no navegador:

```txt
http://127.0.0.1:8000/colaboradores/
```

---

# Integração com Docker

O projeto pode ser containerizado utilizando Docker, garantindo padronização do ambiente e facilidade na implantação.

## Exemplo de Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

# Objetivos do Projeto

- Automatizar o gerenciamento de EPIs
- Melhorar o controle de empréstimos
- Garantir rastreabilidade das operações
- Reduzir falhas humanas
- Auxiliar processos de auditoria

---

# Licença

Este projeto foi desenvolvido para fins acadêmicos e educacionais.