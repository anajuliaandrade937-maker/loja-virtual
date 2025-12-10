from app.extensions import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    imagem = db.Column(db.String(255))

    avaliacoes = db.relationship("Review", back_populates="produto", lazy=True)

    def __repr__(self):
        return f"<Product {self.nome}>"
