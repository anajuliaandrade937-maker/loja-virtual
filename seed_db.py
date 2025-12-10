#!/usr/bin/env python
"""Script para popular o banco de dados com dados de teste"""

import os
import sys
from app import create_app
from app.extensions import db
from app.models.product import Product
from app.models.user import User

def seed_database():
    """Popula o banco com dados de teste"""
    app = create_app()
    
    with app.app_context():
        # Limpar banco anterior (apenas em desenvolvimento)
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
                estoque=5,
                imagem=None
            ),
            Product(
                nome="Mouse Sem Fio",
                descricao="Mouse ergonômico com bateria de longa duração",
                preco=89.90,
                estoque=15,
                imagem=None
            ),
            Product(
                nome="Teclado Mecânico RGB",
                descricao="Teclado mecânico com iluminação RGB customizável",
                preco=250.00,
                estoque=8,
                imagem=None
            ),
            Product(
                nome="Monitor 27 polegadas",
                descricao="Monitor Full HD 144Hz para gaming",
                preco=899.90,
                estoque=3,
                imagem=None
            ),
            Product(
                nome="Webcam HD",
                descricao="Webcam 1080p com microfone integrado",
                preco=129.90,
                estoque=12,
                imagem=None
            ),
            Product(
                nome="Headset Gamer",
                descricao="Headset com som surround 7.1 e microfone retrátil",
                preco=199.90,
                estoque=7,
                imagem=None
            ),
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        
        print("✅ Banco de dados populado com sucesso!")
        print(f"   - 1 usuário criado (joao@example.com / senha123)")
        print(f"   - {len(products)} produtos criados")
        print("\n💾 Dados de teste adicionados ao banco de dados.")

if __name__ == "__main__":
    seed_database()
