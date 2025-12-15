from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.services.product_service import ProductService, CartService, OrderService, ShippingService

# Blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
catalog_bp = Blueprint('catalog', __name__, url_prefix='/catalog')
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
order_bp = Blueprint('order', __name__, url_prefix='/orders')
review_bp = Blueprint('review', __name__, url_prefix='/reviews')
main_bp = Blueprint('main', __name__)

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from app.models.user import User
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        if not all([nome, email, senha, confirmar_senha]):
            flash('Todos os campos são obrigatórios', 'danger')
            return redirect(url_for('auth.register'))
        
        if senha != confirmar_senha:
            flash('As senhas não conferem', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(nome=nome, email=email)
        user.set_senha(senha)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app.models.user import User
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if not email or not senha:
            flash('Email e senha são obrigatórios', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_senha(senha):
            flash('Email ou senha inválidos', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        flash(f'Bem-vindo, {user.nome}!', 'success')
        return redirect(url_for('catalog.index'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado', 'info')
    return redirect(url_for('main.home'))


# ==================== ROTAS DO CATÁLOGO ====================

@main_bp.route('/')
def home():
    """Página inicial com produtos em destaque"""
    from app.models.product import Product
    products = Product.query.limit(6).all()
    return render_template('index.html', products=products)


@catalog_bp.route('/')
def index():
    """Lista todos os produtos com paginação"""
    page = request.args.get('page', 1, type=int)
    products = ProductService.get_all_products(page=page)
    return render_template('catalog/index.html', products=products)


@catalog_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Detalhes de um produto"""
    from app.models.review import Review
    
    product = ProductService.get_product_by_id(product_id)
    if not product:
        flash('Produto não encontrado', 'danger')
        return redirect(url_for('catalog.index'))
    
    reviews = Review.query.filter_by(produto_id=product_id).all()
    avg_rating = ProductService.get_average_rating(product_id)
    
    return render_template('catalog/product_detail.html', 
                         product=product, 
                         reviews=reviews, 
                         avg_rating=avg_rating)


@catalog_bp.route('/search')
def search():
    """Busca de produtos"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return redirect(url_for('catalog.index'))
    
    products = ProductService.search_products(query, page=page)
    return render_template('catalog/search.html', products=products, query=query)


# ==================== ROTAS DO CARRINHO ====================

@cart_bp.route('/')
@login_required
def view():
    """Visualiza o carrinho"""
    cart_items = CartService.get_user_cart(current_user.id)
    total = CartService.get_cart_total(current_user.id)
    return render_template('cart/index.html', items=cart_items, total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_item(product_id):
    """Adiciona um item ao carrinho"""
    product = ProductService.get_product_by_id(product_id)
    if not product:
        flash('Produto não encontrado', 'danger')
        return redirect(url_for('catalog.index'))
    
    quantidade = request.form.get('quantidade', 1, type=int)
    if quantidade < 1:
        quantidade = 1
    
    if product.estoque < quantidade:
        flash('Quantidade indisponível em estoque', 'danger')
        return redirect(url_for('catalog.product_detail', product_id=product_id))
    
    CartService.get_or_create_cart_item(current_user.id, product_id, quantidade)
    flash(f'{product.nome} adicionado ao carrinho!', 'success')
    
    return redirect(request.referrer or url_for('catalog.index'))


@cart_bp.route('/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_item(cart_item_id):
    """Remove um item do carrinho"""
    CartService.remove_from_cart(cart_item_id, current_user.id)
    flash('Item removido do carrinho', 'success')
    return redirect(url_for('cart.view'))


@cart_bp.route('/update/<int:cart_item_id>', methods=['POST'])
@login_required
def update_item(cart_item_id):
    """Atualiza a quantidade de um item"""
    quantidade = request.form.get('quantidade', 1, type=int)
    CartService.update_cart_item(cart_item_id, quantidade, current_user.id)
    flash('Carrinho atualizado', 'success')
    return redirect(url_for('cart.view'))


@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear():
    """Limpa o carrinho"""
    CartService.clear_cart(current_user.id)
    flash('Carrinho limpo', 'success')
    return redirect(url_for('cart.view'))


# ==================== ROTAS DE PEDIDOS ====================

@order_bp.route('/checkout')
@login_required
def checkout():
    """Página de checkout"""
    cart_items = CartService.get_user_cart(current_user.id)
    if not cart_items:
        flash('Carrinho vazio', 'warning')
        return redirect(url_for('catalog.index'))
    
    subtotal = CartService.get_cart_total(current_user.id)
    shipping_methods = ShippingService.get_shipping_methods()
    
    return render_template('order/checkout.html', 
                         items=cart_items, 
                         subtotal=subtotal,
                         shipping_methods=shipping_methods)


@order_bp.route('/confirm', methods=['POST'])
@login_required
def confirm():
    """Confirma o pedido"""
    cart_items = CartService.get_user_cart(current_user.id)
    if not cart_items:
        flash('Carrinho vazio', 'danger')
        return redirect(url_for('catalog.index'))
    
    # Aqui você integraria com um gateway de pagamento real
    # Por enquanto, apenas cria o pedido
    order = OrderService.create_order_from_cart(current_user.id)
    
    if order:
        flash(f'Pedido #{order.id} realizado com sucesso!', 'success')
        return redirect(url_for('order.detail', order_id=order.id))
    
    flash('Erro ao criar pedido', 'danger')
    return redirect(url_for('order.checkout'))


@order_bp.route('/')
@login_required
def list_orders():
    """Lista todos os pedidos do usuário"""
    orders = OrderService.get_user_orders(current_user.id)
    return render_template('order/list.html', orders=orders)


@order_bp.route('/<int:order_id>')
@login_required
def detail(order_id):
    """Detalhes de um pedido"""
    order = OrderService.get_order_by_id(order_id, current_user.id)
    if not order:
        flash('Pedido não encontrado', 'danger')
        return redirect(url_for('order.list_orders'))
    
    return render_template('order/detail.html', order=order)


# ==================== ROTAS DE AVALIAÇÕES ====================

@review_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    """Adiciona uma avaliação a um produto"""
    from app.models.review import Review
    
    product = ProductService.get_product_by_id(product_id)
    if not product:
        flash('Produto não encontrado', 'danger')
        return redirect(url_for('catalog.index'))
    
    rating = request.form.get('rating', type=int)
    comentario = request.form.get('comentario', '').strip()
    
    if not rating or rating < 1 or rating > 5:
        flash('Avaliação inválida', 'danger')
        return redirect(url_for('catalog.product_detail', product_id=product_id))
    
    review = Review(
        usuario_id=current_user.id,
        produto_id=product_id,
        rating=rating,
        comentario=comentario
    )
    
    db.session.add(review)
    db.session.commit()
    
    flash('Avaliação registrada com sucesso!', 'success')
    return redirect(url_for('catalog.product_detail', product_id=product_id))


def register_blueprints(app):
    """Registra todos os blueprints na aplicação"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(review_bp)


@main_bp.route('/info')
def info():
    """Página de informações do projeto"""
    return render_template('info.html')
