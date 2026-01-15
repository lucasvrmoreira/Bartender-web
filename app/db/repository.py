from psycopg2.extras import execute_values
from app.logger import logger
from app.db.connection import get_conn


def upsert_item(codigo, descricao, lote, status, validade):
    conn = get_conn()
    cur = conn.cursor()
    try:
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
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

# 2. ADICIONA ESTA NOVA (Para o Power Automate/Lote)
def upsert_lote_db(lista_itens):
    conn = get_conn()
    cur = conn.cursor()
    try:
        logger.info(f"Processando lote de {len(lista_itens)} itens.")
        query = """
            INSERT INTO cellavita ("Codigo", "Descricao", "Lote", "Status", "Validade")
            VALUES %s
            ON CONFLICT ("Codigo", "Lote")
            DO UPDATE SET
                "Descricao" = EXCLUDED."Descricao",
                "Status" = EXCLUDED."Status",
                "Validade" = EXCLUDED."Validade"
        """
        execute_values(cur, query, lista_itens)
        conn.commit()
        logger.info("Lote processado com sucesso!")
    except Exception:
        conn.rollback()
        logger.error("Erro no processamento em lote", exc_info=True)
        raise
    finally:
        cur.close()
        conn.close()