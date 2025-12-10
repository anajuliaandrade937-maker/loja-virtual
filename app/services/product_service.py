from app.extensions import db
from flask import current_app


class ProductService:
    """Serviço para gerenciar produtos"""
    
    @staticmethod
    def get_all_products(page=1, per_page=None):
        """Retorna lista paginada de todos os produtos"""
        from app.models.product import Product
        per_page = per_page or current_app.config['ITEMS_PER_PAGE']
        return Product.query.paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_product_by_id(product_id):
        """Retorna um produto pelo ID"""
        from app.models.product import Product
        return Product.query.get(product_id)
    
    @staticmethod
    def search_products(query, page=1, per_page=None):
        """Busca produtos por nome ou descrição"""
        from app.models.product import Product
        per_page = per_page or current_app.config['ITEMS_PER_PAGE']
        return Product.query.filter(
            (Product.nome.ilike(f"%{query}%")) | 
            (Product.descricao.ilike(f"%{query}%"))
        ).paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_average_rating(product_id):
        """Calcula a média de avaliações de um produto"""
        from app.models.review import Review
        avg = db.session.query(db.func.avg(Review.rating)).filter(
            Review.produto_id == product_id
        ).scalar()
        return round(avg, 1) if avg else 0


class CartService:
    """Serviço para gerenciar carrinho de compras"""
    
    @staticmethod
    def get_or_create_cart_item(user_id, product_id, quantidade=1):
        """Obtém ou cria um item no carrinho"""
        from app.models.cart_item import CartItem
        item = CartItem.query.filter_by(usuario_id=user_id, product_id=product_id).first()
        
        if item:
            item.quantidade += quantidade
        else:
            item = CartItem(usuario_id=user_id, product_id=product_id, quantidade=quantidade)
            db.session.add(item)
        
        db.session.commit()
        return item
    
    @staticmethod
    def remove_from_cart(cart_item_id, user_id):
        """Remove um item do carrinho"""
        from app.models.cart_item import CartItem
        item = CartItem.query.filter_by(id=cart_item_id, usuario_id=user_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
        return item
    
    @staticmethod
    def get_user_cart(user_id):
        """Retorna todos os itens do carrinho do usuário"""
        from app.models.cart_item import CartItem
        return CartItem.query.filter_by(usuario_id=user_id).all()
    
    @staticmethod
    def clear_cart(user_id):
        """Limpa o carrinho do usuário"""
        from app.models.cart_item import CartItem
        CartItem.query.filter_by(usuario_id=user_id).delete()
        db.session.commit()
    
    @staticmethod
    def get_cart_total(user_id):
        """Calcula o total do carrinho"""
        from app.models.cart_item import CartItem
        items = CartItem.query.filter_by(usuario_id=user_id).all()
        return sum(item.subtotal() for item in items)
    
    @staticmethod
    def update_cart_item(cart_item_id, quantidade, user_id):
        """Atualiza a quantidade de um item no carrinho"""
        from app.models.cart_item import CartItem
        item = CartItem.query.filter_by(id=cart_item_id, usuario_id=user_id).first()
        if item:
            if quantidade <= 0:
                db.session.delete(item)
            else:
                item.quantidade = quantidade
            db.session.commit()
        return item


class OrderService:
    """Serviço para gerenciar pedidos"""
    
    @staticmethod
    def create_order_from_cart(user_id):
        """Cria um pedido a partir do carrinho"""
        from app.models.cart_item import CartItem
        from app.models.order import Order
        from app.models.order_item import OrderItem
        
        cart_items = CartItem.query.filter_by(usuario_id=user_id).all()
        
        if not cart_items:
            return None
        
        # Calcula o total
        total = sum(item.subtotal() for item in cart_items)
        
        # Cria o pedido
        order = Order(usuario_id=user_id, total=total, status="CONFIRMADO")
        db.session.add(order)
        db.session.flush()  # Para obter o ID do pedido
        
        # Cria os itens do pedido
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantidade=item.quantidade,
                preco=item.produto.preco
            )
            # Reduz o estoque
            item.produto.estoque -= item.quantidade
            db.session.add(order_item)
        
        # Limpa o carrinho
        CartService.clear_cart(user_id)
        
        db.session.commit()
        return order
    
    @staticmethod
    def get_user_orders(user_id):
        """Retorna todos os pedidos de um usuário"""
        from app.models.order import Order
        return Order.query.filter_by(usuario_id=user_id).order_by(Order.criado_em.desc()).all()
    
    @staticmethod
    def get_order_by_id(order_id, user_id=None):
        """Retorna um pedido pelo ID"""
        from app.models.order import Order
        query = Order.query.filter_by(id=order_id)
        if user_id:
            query = query.filter_by(usuario_id=user_id)
        return query.first()
    
    @staticmethod
    def update_order_status(order_id, status):
        """Atualiza o status de um pedido"""
        from app.models.order import Order
        order = Order.query.get(order_id)
        if order:
            order.status = status
            db.session.commit()
        return order


class ShippingService:
    """Serviço para calcular frete (simulado)"""
    
    SHIPPING_RATES = {
        'standard': 15.00,
        'express': 30.00,
        'overnight': 50.00
    }
    
    @staticmethod
    def calculate_shipping(total, method='standard'):
        """Calcula o frete baseado no método de envio"""
        base_rate = ShippingService.SHIPPING_RATES.get(method, 15.00)
        
        # Frete grátis para pedidos acima de R$ 100
        if total >= 100:
            return 0.00
        
        return base_rate
    
    @staticmethod
    def get_shipping_methods():
        """Retorna os métodos de envio disponíveis"""
        return {
            'standard': {'name': 'Envio Padrão', 'days': '5-7', 'price': 'A partir de R$ 15'},
            'express': {'name': 'Envio Express', 'days': '2-3', 'price': 'A partir de R$ 30'},
            'overnight': {'name': 'Envio Noturno', 'days': '1', 'price': 'A partir de R$ 50'}
        }
