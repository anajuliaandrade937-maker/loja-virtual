from flask import Flask
from app.extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.DevelopmentConfig")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Carregar o usuário para flask_login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Registrar blueprints - lazy para evitar circular import
    with app.app_context():
        # Importar todos os modelos aqui para garantir que o SQLAlchemy registre
        # todos os mappers e resolva relacionamentos nomeados (Review, Order, etc.)
        # antes de qualquer query ser executada pelas rotas. Use importlib to avoid
        # sobrescrever a variável local `app` (que é a instância Flask).
        import importlib
        importlib.import_module('app.models.user')
        importlib.import_module('app.models.product')
        importlib.import_module('app.models.order')
        importlib.import_module('app.models.order_item')
        importlib.import_module('app.models.cart_item')
        importlib.import_module('app.models.review')
        from app.routes.main import register_blueprints
        register_blueprints(app)
    
    # Criar as pastas de upload se não existirem
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
