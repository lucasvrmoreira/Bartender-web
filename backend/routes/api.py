# backend/routes/api.py
import re
from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_, desc
from pydantic import BaseModel

from backend.db.database import get_db
from backend.db.models import Item
from backend.services.status import normalizar_status
from backend.logger import logger

# Cria o roteador (Substitui o Blueprint do Flask)
router = APIRouter()

PREFIXO_LOTE = "LIC'"

# --- PYDANTIC SCHEMAS (A magia da validação automática) ---
class ItemBase(BaseModel):
    codigo: str
    lote: str
    descricao: str
    status: str
    validade: Optional[str] = None # Aceita string ("20/03/2026") ou None

class LoteImportacao(BaseModel):
    itens: List[ItemBase]

# --- FUNÇÕES AUXILIARES ---
def converter_data_str_para_date(data_raw: str) -> Optional[date]:
    if not data_raw:
        return None
    try:
        return datetime.strptime(data_raw, "%d/%m/%Y").date()
    except ValueError:
        return None

# --- ROTAS ---

@router.post("/api/importar-item")
async def importar_item(item_data: ItemBase, db: AsyncSession = Depends(get_db)):
    """Recebe um JSON já validado pelo Pydantic (item_data)"""
    try:
        validade = converter_data_str_para_date(item_data.validade)
        status_norm = normalizar_status(item_data.status)

        # Busca assíncrona
        stmt = select(Item).where(Item.Codigo == item_data.codigo, Item.Lote == item_data.lote)
        result = await db.execute(stmt)
        item_bd = result.scalars().first()

        if item_bd:
            item_bd.Descricao = item_data.descricao
            item_bd.Status = status_norm
            item_bd.Validade = validade
        else:
            novo_item = Item(
                Codigo=item_data.codigo,
                Descricao=item_data.descricao,
                Lote=item_data.lote,
                Status=status_norm,
                Validade=validade
            )
            db.add(novo_item)

        await db.commit()
        return {"status": "ok"}

    except Exception as e:
        await db.rollback()
        logger.error(f"ERRO CRÍTICO na rota importar-item: {e}")
        raise HTTPException(status_code=500, detail="Falha interna no servidor.")


@router.get("/api/itens")
async def listar_itens(db: AsyncSession = Depends(get_db)):
    try:
        # Busca os últimos 50 itens (Assíncrono)
        stmt = select(Item).order_by(desc(Item.id)).limit(50)
        result = await db.execute(stmt)
        itens = result.scalars().all()
        
        lista = [{
            "id": i.id,
            "codigo": i.Codigo,
            "descricao": i.Descricao,
            "lote": i.Lote,
            "validade": i.Validade.strftime("%d/%m/%Y") if i.Validade else None,
            "status": i.Status
        } for i in itens]

        return lista # O FastAPI converte dicionários/listas para JSON automaticamente!

    except Exception as e:
        logger.error(f"ERRO CRÍTICO na rota listar-itens: {e}")
        raise HTTPException(status_code=500, detail="Falha interna ao buscar itens.")


@router.get("/api/buscar")
async def buscar_lotes(lotes: str = "", db: AsyncSession = Depends(get_db)):
    if not lotes.strip():
        return []

    numeros = re.findall(r"\d+", lotes)
    lotes_formatados = [f"{PREFIXO_LOTE}{n}" for n in numeros]

    try:
        stmt = select(Item).where(Item.Lote.in_(lotes_formatados))
        result = await db.execute(stmt)
        resultados = result.scalars().all()
        
        lista = [{
            "id": i.id,
            "codigo": i.Codigo,
            "descricao": i.Descricao,
            "lote": i.Lote,
            "validade": i.Validade.strftime("%d/%m/%Y") if i.Validade else None
        } for i in resultados]
        
        return lista

    except Exception as e:
        logger.error(f"ERRO CRÍTICO na rota buscar-lotes: {e}")
        raise HTTPException(status_code=500, detail="Falha interna na busca.")