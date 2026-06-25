# Construção de REST API com Python

Projeto desenvolvido com o objetivo de praticar conceitos fundamentais de desenvolvimento Backend utilizando Python, FastAPI, SQLAlchemy e autenticação JWT.

O sistema simula uma API de gerenciamento de usuários e pedidos, permitindo o estudo de:

- Criação de APIs REST
- Autenticação com JWT
- Controle de permissões
- Modelagem de banco de dados relacional
- Relacionamentos com SQLAlchemy
- Schemas com Pydantic
- Documentação automática com Swagger

---

## Tecnologias Utilizadas

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT (JSON Web Token)
- Uvicorn

---

## Funcionalidades

### Usuários

- Cadastro de usuários
- Login com geração de Token JWT
- Consulta de usuários
- Controle de permissões administrativas

### Pedidos

- Criação de pedidos
- Visualização de pedidos
- Listagem de pedidos por usuário
- Cancelamento de pedidos
- Finalização de pedidos

### Itens de Pedido

- Inclusão de itens em pedidos
- Remoção de itens
- Cálculo automático do valor total do pedido

---

## Estrutura do Projeto

```text
.
├── main.py
├── models.py
├── schemas.py
├── dependencias.py
├── auth_rotas.py
├── ordens_rotas.py
└── banco.db
