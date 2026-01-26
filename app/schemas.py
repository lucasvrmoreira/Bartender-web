# app/schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# 1. O Modelo Base (Campos comuns)
class ItemBase(BaseModel):
    Codigo: str
    Descricao: str
    Lote: str
    Status: str
    Validade: Optional[date] = None

# 2. O Modelo de Leitura (Inclui o ID que vem do banco)
class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True

# 3. --- ATUALIZADO: Schema para o Pedido de Impressão ---
class PrintRequest(BaseModel):
    lotes: List[str]          # Lista de lotes obrigatória
    modelo: str = "67x26"     # Padrão, mas o front pode mandar outro
    copias: int = 1           # Quantidade de cópias
    printer_name: Optional[str] = None # Mantive o seu, caso use no futuro
    
class ItemImport(BaseModel):
    codigo: str
    lote: str
    descricao: Optional[str] = None
    status: Optional[str] = None
    validade: Optional[str] = None # Recebe string "DD/MM/YYYY"

class LoteImportRequest(BaseModel):
    itens: List[ItemImport]