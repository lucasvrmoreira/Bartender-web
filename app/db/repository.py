from app.logger import logger
from app.db.connection import get_conn


def upsert_item(codigo, descricao, lote, status, validade):
    conn = get_conn()
    cur = conn.cursor()

    try:
        logger.debug(
            "Executando upsert_item",
            extra={"codigo": codigo, "lote": lote}
        )

        cur.execute("""
            INSERT INTO cellavita ("Codigo", "Descricao", "Lote", "Status", "Validade")
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT ("Codigo", "Lote")
            DO UPDATE SET
                "Descricao" = EXCLUDED."Descricao",
                "Status" = EXCLUDED."Status",
                "Validade" = EXCLUDED."Validade"
        """, (codigo, descricao, lote, status, validade))

        conn.commit()

        logger.info(
            "Upsert realizado com sucesso",
            extra={"codigo": codigo, "lote": lote}
        )

    except Exception:
        conn.rollback()
        logger.error(
            "Erro ao realizar upsert_item",
            exc_info=True,
            extra={"codigo": codigo, "lote": lote}
        )
        raise

    finally:
        cur.close()
        conn.close()
