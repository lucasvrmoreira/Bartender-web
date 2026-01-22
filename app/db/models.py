"Esse sera nosso dicionario de modelos, substituindo o uso direto de SQL em varias partes do codigo"


from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
# Importa o 'Base' que criamos no arquivo database.py
from app.db.database import Base 

class Item(Base):
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