from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint

# Inicializamos o db aqui para ser usado em toda a aplicação
db = SQLAlchemy()

class Item(db.Model):  # AQUI ESTÁ A CHAVE: Mude de (Base) para (db.Model)
    __tablename__ = 'cellavita'
    
    __table_args__ = (
        UniqueConstraint('Codigo', 'Lote', name='uix_codigo_lote'),
        {'schema': 'barthenderweb'} 
    )

    id = Column(Integer, primary_key=True)
    Codigo = Column(String, nullable=False)
    Descricao = Column(String, nullable=False)
    Lote = Column(String, nullable=False)
    Status = Column(String, nullable=False)
    Validade = Column(Date, nullable=True)