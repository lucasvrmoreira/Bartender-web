
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
from backend.db.database import Base  

class Item(Base):  
    __tablename__ = 'cellavita'
    
    __table_args__ = (
        UniqueConstraint('Codigo', 'Lote', name='uix_codigo_lote'),
        {'schema': 'barthenderweb'} 
    )

    # Em Python, variáveis devem ser minúsculas (snake_case).
    id = Column(Integer, primary_key=True)
    Codigo = Column(String, nullable=False)
    Descricao = Column(String, nullable=False)
    Lote = Column(String, nullable=False)
    Status = Column(String, nullable=False)
    Validade = Column(Date, nullable=True)