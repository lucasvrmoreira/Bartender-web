"Esse sera nosso dicionario de modelos, substituindo o uso direto de SQL em varias partes do codigo"

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'cellavita'
    
    # Esta linha é o segredo para resolver o UndefinedTable
    __table_args__ = (
        db.UniqueConstraint('Codigo', 'Lote', name='uix_codigo_lote'),
        {'schema': 'barthenderweb'} # <--- Adicione isso aqui!
    )

    id = db.Column(db.Integer, primary_key=True)
    Codigo = db.Column(db.String, nullable=False)
    Descricao = db.Column(db.String, nullable=False)
    Lote = db.Column(db.String, nullable=False)
    Status = db.Column(db.String, nullable=False)
    Validade = db.Column(db.Date, nullable=True)

