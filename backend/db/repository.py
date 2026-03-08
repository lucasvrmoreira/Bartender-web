from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.models import Item
from backend.logger import logger

async def upsert_item(db: AsyncSession, codigo: str, descricao: str, lote: str, status: str, validade):
    try:
        stmt = select(Item).where(Item.Codigo == codigo, Item.Lote == lote)
        
        result = await db.execute(stmt)
        item = result.scalars().first()

        if item:
            item.Descricao = descricao
            item.Status = status
            item.Validade = validade
            item_salvo = item # Guarda a referência do item atualizado
        else:
            novo_item = Item(
                Codigo=codigo,
                Descricao=descricao,
                Lote=lote,
                Status=status,
                Validade=validade
            )
            db.add(novo_item) 
            item_salvo = novo_item # Guarda a referência do item novo
        
        await db.commit()
        
        # Opcional, mas muito recomendado no Async: 
        # Dá um "refresh" para garantir que o SQLAlchemy carregou o ID gerado pelo banco para o item_salvo
        await db.refresh(item_salvo) 
        
        return item_salvo
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Erro no upsert: {e}")
        raise e