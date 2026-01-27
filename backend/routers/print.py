# app/routers/print.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.models import Item
from app.schemas import PrintRequest
from app.utils.datas import formatar_data_br


from app.services.etiqueta.factory import gerar_zpl_por_modelo
from app.services.print_agent import enviar_para_agente

router = APIRouter(prefix="/print", tags=["Impressão"])

# ROTA 1: Imprimir por ID (Ex: /print/item/150)
@router.post("/item/{id}")
async def imprimir_item_unico(
    id: int, 
    modelo: str = "67x26", 
    qtd: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    # Busca Async no banco
    item = await db.get(Item, id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    try:
        # Gera o código ZPL
        zpl = gerar_zpl_por_modelo(
            modelo=modelo,
            codigo=item.Codigo,
            descricao=item.Descricao,
            lote=item.Lote,
            validade=formatar_data_br(item.Validade)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao gerar etiqueta: {str(e)}")

    # Envia para a impressora
    sucesso = enviar_para_agente(zpl, copies=qtd)

    if not sucesso:
        raise HTTPException(status_code=503, detail="Agente de impressão offline.")

    return {"status": "success", "message": f"Item {item.Codigo} enviado para impressão"}


# ROTA 2: Imprimir Lote (Payload JSON)
@router.post("/batch")
async def imprimir_lote_lista(
    request: PrintRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Recebe uma lista de lotes e imprime todos de uma vez.
    Usa o modelo e cópias definidos no JSON.
    """
    if not request.lotes:
        raise HTTPException(status_code=400, detail="A lista de lotes está vazia")

    # Busca todos os itens de uma vez (SELECT * FROM item WHERE lote IN (...))
    stmt = select(Item).where(Item.Lote.in_(request.lotes))
    result = await db.execute(stmt)
    itens = result.scalars().all()

    if not itens:
        raise HTTPException(status_code=404, detail="Nenhum item encontrado para os lotes informados")

    zpl_total = ""
    contador = 0

    # Gera um ZPL grandão com todas as etiquetas
    for item in itens:
        try:
            zpl = gerar_zpl_por_modelo(
                modelo=request.modelo,
                codigo=item.Codigo,
                descricao=item.Descricao,
                lote=item.Lote,
                validade=formatar_data_br(item.Validade)
            )
            zpl_total += zpl + "\n"
            contador += 1
        except Exception:
            continue # Se um falhar, pula pro próximo

    if zpl_total:
        sucesso = enviar_para_agente(zpl_total, copies=request.copias)
        if not sucesso:
            raise HTTPException(status_code=503, detail="Falha ao enviar para o agente de impressão")
            
        return {
            "status": "success", 
            "enviados": contador, 
            "total_solicitado": len(request.lotes)
        }
    
    raise HTTPException(status_code=400, detail="Não foi possível gerar nenhuma etiqueta válida")