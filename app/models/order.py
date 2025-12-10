from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="PENDENTE")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("OrderItem", back_populates="pedido", lazy=True)
    usuario = db.relationship("User", back_populates="pedidos")

    def __repr__(self):
        return f"<Order {self.id}>"
