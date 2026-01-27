from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.models import Item
from backend.logger import logger


async def upsert_item(db: AsyncSession, codigo: str, descricao: str, lote: str, status: str, validade):
    try:
        # 1. Busca Assíncrona (Substitui o Item.query.filter_by)
        # "Selecione o Item onde Codigo é igual a X e Lote é igual a Y"
        stmt = select(Item).where(Item.Codigo == codigo, Item.Lote == lote)
        
        # Executa a query no banco esperando a resposta (await)
        result = await db.execute(stmt)
        item = result.scalars().first()

        if item:
            # 2. Se existe, atualizamos (UPDATE)
            item.Descricao = descricao
            item.Status = status
            item.Validade = validade
        else:
            # 3. Se não existe, criamos um novo (INSERT)
            novo_item = Item(
                Codigo=codigo,
                Descricao=descricao,
                Lote=lote,
                Status=status,
                Validade=validade
            )
            db.add(novo_item) # Adiciona na memória da sessão
        
        # 4. Commit para salvar as mudanças no banco
        await db.commit()
        
        return item
        
    except Exception as e:
        # Se der erro, desfaz tudo
        await db.rollback()
        logger.error(f"Erro no upsert: {e}")
        raise e