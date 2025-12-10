#!/usr/bin/env python
"""Script para popular o banco de dados com dados de teste"""

import sys
sys.path.insert(0, '.')

def seed():
    from app import create_app
    from app.extensions import db
    # Import all models first so SQLAlchemy can register mappers and resolve relationships
    from app.models.user import User
    from app.models.product import Product
    from app.models.order import Order
    from app.models.order_item import OrderItem
    from app.models.cart_item import CartItem
    from app.models.review import Review
    
    app = create_app()
    
    with app.app_context():
        # Limpar banco anterior
        db.drop_all()
        db.create_all()
        
        # Criar usuário de teste
        user = User(
            nome="João Silva",
            email="joao@example.com"
        )
        user.set_senha("senha123")
        db.session.add(user)
        
        # Criar produtos de teste
        products = [
            Product(
                nome="Notebook Gamer",
                descricao="Notebook com processador Intel i7, 16GB RAM, GTX 1660",
                preco=3500.00,
                estoque=5
            ),
            Product(
                nome="Mouse Sem Fio",
                descricao="Mouse ergonômico com bateria de longa duração",
                preco=89.90,
                estoque=15
            ),
            Product(
                nome="Teclado Mecânico RGB",
                descricao="Teclado mecânico com iluminação RGB customizável",
                preco=250.00,
                estoque=8
            ),
            Product(
                nome="Monitor 27 polegadas",
                descricao="Monitor IPS 27 polegadas, resolução 4K, 60Hz",
                preco=1200.00,
                estoque=10
            ),
            Product(
                nome="Webcam HD",
                descricao="Webcam Full HD com microfone integrado",
                preco=150.00,
                estoque=20
            ),
            Product(
                nome="Headset Gamer",
                descricao="Headset com som surround 7.1, microfone desmontável",
                preco=350.00,
                estoque=12
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print("✅ Banco de dados populado com sucesso!")
        print(f"✓ 1 usuário criado: joao@example.com / senha123")
        print(f"✓ 6 produtos criados")

if __name__ == "__main__":
    seed()
