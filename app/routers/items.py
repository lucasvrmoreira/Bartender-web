# app/routers/items.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

# Imports do seu projeto
from app.db.database import get_db
from app.db.models import Item
from app.schemas import ItemResponse

router = APIRouter(prefix="/items", tags=["Itens"])

# GET /items/ -> Lista todos os itens (limitado a 50 pra não travar)
@router.get("/", response_model=List[ItemResponse])
async def listar_itens(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    # Query Async: Selecione Itens...
    stmt = select(Item).offset(skip).limit(limit)
    
    # ...Execute no banco...
    result = await db.execute(stmt)
    
    # ...E me dê os escalares (os objetos Item puros)
    itens = result.scalars().all()
    return itens