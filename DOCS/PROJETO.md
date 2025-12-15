# Projeto: Loja Virtual — Visão Geral e Guia de Execução 🛍️

## 📌 Resumo do Projeto
Este repositório contém uma aplicação web de loja virtual (e‑commerce) construída com Flask. A aplicação oferece catálogo de produtos, carrinho de compras, checkout simulado, histórico de pedidos, avaliações de produtos e autenticação de usuários.

O objetivo é servir como base para um e‑commerce didático e extensível para integrações reais (pagamentos, transportadoras, analytics, etc.).

---

## 🧭 Jornada do Cliente (UX)
1. Descoberta: o cliente chega por busca/marketing.
2. Pesquisa/Navegação: explora o catálogo e páginas de produto.
3. Decisão: adiciona itens ao carrinho.
4. Pagamento: faz checkout (simulado nesta versão).
5. Recebimento e Pós‑venda: pedido é preparado e usuário pode deixar avaliação.

---

## 🔑 Pilares do Negócio
- **Plataforma**: infraestrutura do site e serviços.
- **Produtos**: catálogo e controle de estoque.
- **Marketing**: aquisição e conversão (fora do escopo do código‑fonte).
- **Logística**: cálculo de frete e integração com transportadoras.
- **Atendimento**: suporte e gestão de pedidos.

---

## ✅ Funcionalidades Implementadas
- Catálogo com listagem, busca e paginação
- Pagina de detalhe com avaliações (nota 1–5) e comentários
- Autenticação de usuários (registro/login/logout) via Flask-Login
- Carrinho de compras (adicionar/atualizar/remover/limpar)
- Checkout simulando criação de pedidos
- Cálculo de frete simples (métodos: standard, express, overnight)
- Serviço de ratings (média das avaliações por produto)
- Templates responsivos (mobile‑first)
- Scripts: `populate_db.py` para popular dados de teste

---

## 🛠️ Tecnologias Usadas
- Python 3.11+ (compatível com 3.13)  
- Flask (2.3.x) — microframework web
- Flask-SQLAlchemy — integração SQLAlchemy com Flask
- SQLAlchemy (2.0.x) — ORM
- Flask-Migrate — migrações (Alembic)
- Flask-Login — gerenciamento de sessão/usuário
- Flask-Bcrypt — hashing de senhas
- SQLite — banco de dados de desenvolvimento
- HTML/CSS (templates Jinja2) — UI responsiva

---

## 🧩 Estrutura do Projeto (resumida)
```
loja-virtual/
├── app/
│   ├── models/         # Modelos (User, Product, Order, OrderItem, CartItem, Review)
│   ├── routes/         # Blueprints e handlers (main.py)
│   ├── services/       # Lógica de negócio (product_service.py)
│   ├── templates/      # Templates Jinja2
│   ├── static/         # CSS, imagens, etc.
│   └── extensions/     # db, migrate, login_manager
├── migrations/         # Migrações Alembic
├── run.py              # Entrypoint (app factory + create_all)
├── populate_db.py      # Script de seed (usuário + produtos)
├── requirements.txt
└── DOCS/PROJETO.md     # (este arquivo)
```

---

## ⚙️ Como rodar localmente (PowerShell)
1) Ative o virtualenv (caso use venv no projeto):
```powershell
cd C:\AnaJulia\loja-virtual
.\.venv\Scripts\Activate.ps1
```

2) Instale dependências (se necessário):
```powershell
pip install -r requirements.txt
```

3) Popular o banco com dados de teste:
```powershell
python populate_db.py
```
Usuário criado: `joao@example.com` / `senha123`

4) Iniciar a aplicação em modo desenvolvimento (debug):
```powershell
python run.py
```
A aplicação ficará disponível em `http://127.0.0.1:5000`.

---

## 🧪 Testes rápidos (smoke tests que pode executar manualmente)
- Registro: `GET /auth/register` → criar novo usuário
- Login: `GET /auth/login` → autenticar
- Catálogo: `GET /catalog/` → ver produtos e paginação
- Carrinho: adicionar um produto e visualizar `GET /cart/`
- Checkout: `GET /orders/checkout` e `POST /orders/confirm` (fluxo simulado)

---

## 🔐 Notas de Segurança e Produção
- Em produção, troque o `SECRET_KEY` e use variáveis de ambiente para segredos.
- Use gateway de pagamento real (Stripe/PayPal/PagSeguro) com integração segura.
- Substitua SQLite por um SGBD robusto (Postgres, MySQL) em produção.
- Use servidor WSGI (Gunicorn/Uvicorn) e um proxy reverso (Nginx).

---

## 📦 Próximas melhorias sugeridas
- Integração com gateway de pagamentos
- Integração com API de transportadora (Correios/3PL)
- Busca avançada com sugestões/autocomplete
- Painel administrativo para gerenciar produtos/pedidos/usuários
- Cobertura de testes automatizados (unit + integration)

---

## ❓ Dúvidas/Como Contribuir
- Para contribuir: crie uma branch por feature, abra PR e descreva as mudanças e testes.
- Se quiser, posso ajudar a adicionar CI (GitHub Actions) e testes automatizados.

---

Se quiser, eu adapto este documento para um template HTML (`app/templates/info.html`) e o adiciono como página estática na aplicação. Quer que eu faça essa conversão agora? ✨
