# app/routers/sync.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.db.database import get_db
from app.db.models import Item
from app.schemas import ItemImport, LoteImportRequest
from app.services.status import normalizar_status # Certifique-se que esse arquivo existe

router = APIRouter(prefix="/api", tags=["Sincronização"])

# Função auxiliar para tratar a data
def parse_data_br(date_str: str | None):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        return None

# ROTA 1: Importar Item Único
@router.post("/importar-item")
async def importar_item(data: ItemImport, db: AsyncSession = Depends(get_db)):
    try:
        validade_obj = parse_data_br(data.validade)

        # 1. Verifica se já existe (Async)
        stmt = select(Item).where(Item.Codigo == data.codigo, Item.Lote == data.lote)
        result = await db.execute(stmt)
        item_existente = result.scalars().first()

        status_norm = normalizar_status(data.status)

        if item_existente:
            # Atualiza
            item_existente.Descricao = data.descricao
            item_existente.Status = status_norm
            item_existente.Validade = validade_obj
        else:
            # Cria Novo
            novo_item = Item(
                Codigo=data.codigo,
                Descricao=data.descricao,
                Lote=data.lote,
                Status=status_norm,
                Validade=validade_obj
            )
            db.add(novo_item)

        await db.commit()
        return {"status": "ok"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ROTA 2: Importar Lote (Vários itens)
@router.post("/importar-lote")
async def importar_lote(payload: LoteImportRequest, db: AsyncSession = Depends(get_db)):
    if not payload.itens:
        raise HTTPException(status_code=400, detail="Lista de itens vazia")

    try:
        for item_data in payload.itens:
            validade_obj = parse_data_br(item_data.validade)

            # Busca se existe
            stmt = select(Item).where(Item.Codigo == item_data.codigo, Item.Lote == item_data.lote)
            result = await db.execute(stmt)
            item_existente = result.scalars().first()

            status_norm = normalizar_status(item_data.status)

            if item_existente:
                # Atualiza
                item_existente.Descricao = item_data.descricao
                item_existente.Status = status_norm
                item_existente.Validade = validade_obj
            else:
                # Cria Novo
                novo_item = Item(
                    Codigo=item_data.codigo,
                    Descricao=item_data.descricao,
                    Lote=item_data.lote,
                    Status=status_norm,
                    Validade=validade_obj
                )
                db.add(novo_item)

        await db.commit()
        return {"status": "ok", "total_processado": len(payload.itens)}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))