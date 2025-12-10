from app.extensions import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)  # 1-5 estrelas
    comentario = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship("User", backref="avaliacoes")
    produto = db.relationship("Product", back_populates="avaliacoes")

    def __repr__(self):
        return f"<Review {self.id} - {self.rating}⭐>"
