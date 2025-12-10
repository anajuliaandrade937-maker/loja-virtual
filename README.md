# 🛍️ LojaVirtual - Aplicação Flask

Uma aplicação de e-commerce completa desenvolvida em Flask com funcionalidades essenciais para uma loja virtual moderna.

## ✨ Funcionalidades Implementadas

### 👥 Autenticação e Usuários
- ✅ Registro de novos usuários
- ✅ Login seguro com senhas criptografadas (bcrypt)
- ✅ Gerenciamento de sessões
- ✅ Recuperação de usuário logado

### 🛒 Carrinho de Compras
- ✅ Adicionar produtos ao carrinho
- ✅ Atualizar quantidade de itens
- ✅ Remover itens do carrinho
- ✅ Calcular subtotal automaticamente
- ✅ Limpar carrinho

### 📦 Catálogo de Produtos
- ✅ Exibição organizada de produtos
- ✅ Busca inteligente por nome e descrição
- ✅ Detalhes completos do produto
- ✅ Verificação de estoque
- ✅ Paginação de resultados

### ⭐ Sistema de Avaliações
- ✅ Deixar avaliações com classificação (1-5 estrelas)
- ✅ Adicionar comentários nas avaliações
- ✅ Calcular média de avaliações
- ✅ Exibir prova social (avaliações de outros clientes)

### 💳 Processamento de Pedidos
- ✅ Checkout com informações de entrega
- ✅ Múltiplos métodos de envio
- ✅ Múltiplas formas de pagamento
- ✅ Cálculo de frete automático
- ✅ Histórico de pedidos por usuário
- ✅ Rastreamento de pedidos

### 🎨 Interface Responsiva
- ✅ Design Mobile-First
- ✅ Totalmente responsivo (funciona em celular, tablet e desktop)
- ✅ Interface intuitiva e fácil de usar

## 🚀 Como Instalar e Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar o repositório
```bash
cd c:\AnaJulia\loja-virtual
```

### Passo 2: Criar um ambiente virtual
```bash
python -m venv venv
```

### Passo 3: Ativar o ambiente virtual
**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Passo 4: Instalar as dependências
```bash
pip install -r requirements.txt
```

### Passo 5: Popular o banco de dados com dados de teste
```bash
python seed_db.py
```

Isso criará:
- Um usuário de teste: `joao@example.com` / `senha123`
- 6 produtos de exemplo

### Passo 6: Executar a aplicação
```bash
python run.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 📊 Estrutura do Projeto

```
loja-virtual/
├── app/
│   ├── models/              # Modelos do banco de dados
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── cart_item.py
│   │   └── review.py
│   ├── routes/              # Rotas e blueprints
│   │   └── main.py
│   ├── services/            # Lógica de negócio
│   │   └── product_service.py
│   ├── templates/           # Templates HTML
│   ├── static/              # Arquivos estáticos (CSS, JS)
│   ├── extensions/          # Extensões do Flask
│   ├── __init__.py
│   └── config.py
├── migrations/              # Migrações do banco
├── tests/                   # Testes (para adicionar)
├── run.py                   # Arquivo principal
├── seed_db.py              # Script para popular dados
└── requirements.txt        # Dependências do projeto
```

## 🔐 Credenciais de Teste

**Email:** joao@example.com  
**Senha:** senha123

## 🛠️ Tecnologias Utilizadas

- **Flask 2.3.3** - Framework web
- **SQLAlchemy 2.0** - ORM para banco de dados
- **Flask-Login 0.6** - Gerenciamento de autenticação
- **Flask-Migrate 4.0** - Migrações de banco de dados
- **Flask-Bcrypt 1.0** - Criptografia de senhas
- **SQLite** - Banco de dados (padrão)

## 📋 Rotas Disponíveis

### Autenticação
- `GET /auth/register` - Página de registro
- `POST /auth/register` - Processar novo registro
- `GET /auth/login` - Página de login
- `POST /auth/login` - Processar login
- `GET /auth/logout` - Logout do usuário

### Catálogo
- `GET /` - Página inicial
- `GET /catalog/` - Listagem de produtos
- `GET /catalog/product/<id>` - Detalhes do produto
- `GET /catalog/search` - Buscar produtos

### Carrinho
- `GET /cart/` - Visualizar carrinho
- `POST /cart/add/<product_id>` - Adicionar ao carrinho
- `POST /cart/remove/<item_id>` - Remover do carrinho
- `POST /cart/update/<item_id>` - Atualizar quantidade
- `POST /cart/clear` - Limpar carrinho

### Pedidos
- `GET /orders/` - Listar pedidos do usuário
- `GET /orders/<id>` - Detalhes do pedido
- `GET /orders/checkout` - Página de checkout
- `POST /orders/confirm` - Confirmar pedido

### Avaliações
- `POST /reviews/add/<product_id>` - Adicionar avaliação

## 💡 Próximas Melhorias

- [ ] Integração com gateway de pagamento real (Stripe, PayPal)
- [ ] Sistema de cupons e descontos
- [ ] Wishlist de produtos favoritos
- [ ] Avaliação e comentários moderados
- [ ] API REST para integração externa
- [ ] Dashboard administrativo
- [ ] Sistema de notificações por email
- [ ] Filtros avançados no catálogo
- [ ] Sistema de recomendações de produtos
- [ ] Análise de vendas e relatórios

## 📝 Notas de Desenvolvimento

### Banco de Dados
Por padrão, a aplicação usa SQLite. O banco é criado automaticamente ao executar `run.py`.

### Modo Debug
A aplicação executa em modo DEBUG durante o desenvolvimento. Desative-o em produção alterando `debug=True` para `debug=False` em `run.py`.

### Segurança
- Altere a `SECRET_KEY` em `app/config.py` antes de ir para produção
- Use variáveis de ambiente para dados sensíveis
- Implemente HTTPS em produção

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"
Certifique-se de que o ambiente virtual está ativado e as dependências estão instaladas:
```bash
pip install -r requirements.txt
```

### Erro: "Address already in use"
A porta 5000 já está em uso. Execute em uma porta diferente:
```bash
python run.py --port 5001
```

### Banco de dados corrompido
Delete `loja_virtual.db` e execute `seed_db.py` novamente.

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. Se todas as dependências estão instaladas
2. Se o banco de dados foi populado
3. Os logs da aplicação (mensagens de erro no terminal)

## 📄 Licença

Este projeto é fornecido como está para fins educacionais.

---

**Desenvolvido com ❤️ em Flask**
