# app/routers/web.py
import re
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import Item

# Configuração dos Templates (Aponta para a pasta HTML)
templates = Jinja2Templates(directory="app/templates")

# Criação do roteador (Isso é o que o main.py procura!)
router = APIRouter(include_in_schema=False)

# 1. Rota Home (Página Inicial)
@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "resultados": None
    })

# 2. Rota de Busca
@router.get("/buscar")
async def buscar(request: Request, numeros: str = "", db: AsyncSession = Depends(get_db)):
    # Lógica de limpar o input (Regex)
    numeros_lista = re.findall(r"\d+", numeros)

    if not numeros_lista:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "resultados": None
        })

    # Adiciona prefixo LIC'
    lotes_formatados = [f"LIC'{n}" for n in numeros_lista]

    # Busca no banco
    stmt = select(Item).where(Item.Lote.in_(lotes_formatados))
    result = await db.execute(stmt)
    resultados = result.scalars().all()

    mensagem = None
    if not resultados:
        mensagem = f"⚠️ Nenhum lote encontrado para: {', '.join(lotes_formatados)}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "resultados": resultados,
        "numeros": numeros,
        "mensagem": mensagem
    })

# 3. Rota de Etiqueta (Preview)
@router.get("/etiqueta/{id}")
async def etiqueta(request: Request, id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(Item, id)

    if not item:
        return "Item não encontrado", 404

    return templates.TemplateResponse("label.html", {
        "request": request,
        "item_id": id,
        "codigo": item.Codigo,
        "descricao": item.Descricao,
        "lote": item.Lote,
        "validade": item.Validade
    })