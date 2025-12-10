import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Criar banco de dados
        from app.extensions import db
        db.create_all()
    
    app.run(debug=True, port=5000)
