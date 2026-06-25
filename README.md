# Construção de REST API com Python

Projeto desenvolvido durante meus estudos do curso de FastAPI da Hashtag Programação, com o objetivo de consolidar conhecimentos em desenvolvimento Backend utilizando Python.

Ao longo do desenvolvimento foram realizadas adaptações, correções e melhorias para aprofundar o entendimento sobre APIs REST, autenticação, banco de dados e organização de projetos.

---

## Objetivos do Projeto

Este projeto foi criado para praticar:

* Desenvolvimento de APIs REST com FastAPI
* Modelagem de banco de dados com SQLAlchemy
* Autenticação utilizando JWT
* Controle de permissões e autorização
* Relacionamentos entre tabelas
* Validação de dados com Pydantic
* Organização de aplicações Backend

---

## Tecnologias Utilizadas

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT
* Uvicorn
---

## Funcionalidades Implementadas

### Usuários

* Cadastro de usuários
* Login com autenticação JWT
* Controle de usuários ativos
* Controle de permissões administrativas

### Pedidos

* Criação de pedidos
* Consulta de pedidos
* Cancelamento de pedidos
* Finalização de pedidos
* Listagem de pedidos por usuário

### Itens de Pedido

* Adição de itens ao pedido
* Remoção de itens
* Atualização automática do valor total do pedido

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
```
---
## Durante este projeto pratiquei:

* Estruturação de APIs REST
* Organização de rotas
* Uso de dependências no FastAPI
* Relacionamentos com SQLAlchemy
* Controle de autenticação e autorização
* Modelagem de banco de dados relacional
* Tratamento de erros HTTP
* Integração entre API e banco de dados
---

## Autor

Thiago Yukio

GitHub:
https://github.com/Thiago-Yukio
