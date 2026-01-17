from app.db.models import db, Item
from app.logger import logger

def upsert_item(codigo, descricao, lote, status, validade):
    try:
        # 1. Procuramos se já existe esse par Codigo/Lote
        item = Item.query.filter_by(codigo=codigo, lote=lote).first()

        if item:
            # 2. Se existe, atualizamos (UPDATE)
            item.descricao = descricao
            item.status = status
            item.validade = validade
        else:
            # 3. Se não existe, criamos um novo (INSERT)
            novo_item = Item(
                codigo=codigo,
                descricao=descricao,
                lote=lote,
                status=status,
                validade=validade
            )
            db.session.add(novo_item)
        
        db.session.commit() # Salva de verdade
    except Exception as e:
        db.session.rollback() # Se der erro, desfaz tudo
        logger.error(f"Erro no upsert: {e}")
        raise