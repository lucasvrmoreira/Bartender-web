"""
Rotas de impressão (Padrão FastAPI).
"""
import re
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.logger import logger
from backend.db.database import get_db
from backend.db.models import Item
from backend.utils.datas import formatar_data_br
from backend.services.etiqueta.factory import gerar_zpl_por_modelo
from backend.services.print_agent import enviar_para_agente

# Substitui o Blueprint do Flask
router = APIRouter()

PREFIXO_LOTE = "LIC'"

# Rota no FastAPI com injeção de dependência e tipagem forte!
@router.get("/api/imprimir/{id}")
async def imprimir_etiqueta(
    id: int, 
    modelo: str = Query("67x26"), 
    qtd: int = Query(1, gt=0), # gt=0 garante que não podem pedir "0" etiquetas
    qrcode: bool = Query(True),
    db: AsyncSession = Depends(get_db)
):
    logger.info("Solicitação de impressão", extra={"id": id})

    try:
        # Busca Assíncrona no Banco (Modo novo)
        item = await db.get(Item, id)
        
        if not item:
            logger.warning("Etiqueta não encontrada", extra={"id": id})
            raise HTTPException(status_code=404, detail="Etiqueta não encontrada")
        
        logger.info("Preparando impressão", extra={"modelo": modelo, "quantidade": qtd, "qrcode": qrcode})

        validade_br = formatar_data_br(item.Validade)
        zpl = gerar_zpl_por_modelo(
            modelo=modelo,
            codigo=item.Codigo,
            descricao=item.Descricao,
            lote=item.Lote,
            validade=validade_br,
            com_qrcode=qrcode
        )
        
        logger.info("Enviando ZPL para agente de impressão")
        sucesso = enviar_para_agente(zpl, qtd)

        if not sucesso:
            logger.error("Agente de impressão OFFLINE ou inacessível")
            raise HTTPException(status_code=503, detail="Agente de impressão offline. Verifique o Zebra Agent.")
        
        logger.info("Impressão concluída com sucesso", extra={"id": id, "quantidade": qtd})
        # O FastAPI converte dicionários para JSON sozinho!
        return {"mensagem": "Etiqueta enviada para a impressora", "quantidade": qtd}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro crítico na impressão individual: {e}")
        raise HTTPException(status_code=500, detail="Falha interna ao processar a impressão.")


@router.get("/api/imprimir-fila")
async def imprimir_fila(
    numeros: str = Query("", description="Lotes separados por vírgula"),
    modelo: str = Query("67x26"),
    qrcode: bool = Query(True),
    db: AsyncSession = Depends(get_db)
):
    try:
        numeros_extraidos = re.findall(r"\d+", numeros)
        if not numeros_extraidos:
            raise HTTPException(status_code=400, detail="Nenhum lote válido informado na URL")

        lotes = [f"{PREFIXO_LOTE}{n}" for n in numeros_extraidos]

        # Busca Assíncrona em Lote
        stmt = select(Item).where(Item.Lote.in_(lotes))
        result = await db.execute(stmt)
        itens = result.scalars().all()

        if not itens:
            raise HTTPException(status_code=404, detail="Nenhum item encontrado para os lotes informados")

        zpl_total = ""
        for item in itens:
            zpl = gerar_zpl_por_modelo(
                modelo=modelo,
                codigo=item.Codigo,
                descricao=item.Descricao,
                lote=item.Lote,
                validade=formatar_data_br(item.Validade),
                com_qrcode=qrcode
            )
            zpl_total += zpl + "\n"

        logger.info("Enviando fila de impressão", extra={"total": len(itens)})
        sucesso = enviar_para_agente(zpl_total)

        if not sucesso:
            logger.error("Agente de impressão OFFLINE (fila)")
            raise HTTPException(status_code=503, detail="Agente de impressão offline. Não foi possível enviar a fila.")

        return {"mensagem": f"Fila enviada com {len(itens)} etiquetas"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro crítico na fila de impressão: {e}")
        raise HTTPException(status_code=500, detail="Falha interna ao processar a fila de impressão.")