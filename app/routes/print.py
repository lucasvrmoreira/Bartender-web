"""
Rotas de impressão.

Responsável por:
- buscar dados no banco
- gerar etiquetas (via factory)
- enviar ZPL para a impressora Zebra
"""



from flask import Blueprint, request
from app.logger import logger
from app.db.connection import get_conn
from app.config import TABELA
from app.utils.datas import formatar_data_br
from app.services.etiqueta.factory import gerar_zpl_por_modelo
from app.services.print_agent import enviar_para_agente


print_bp = Blueprint("print", __name__)


@print_bp.route("/imprimir/<int:id>")
def imprimir(id):
    
    logger.info("Solicitação de impressão", extra={"id": id})

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT "Codigo", "Descricao", "Lote", "Validade" as validade
        FROM {TABELA}
        WHERE id = %s
    """, (id,))

    item = cur.fetchone()
    conn.close()

    
    if not item:
        logger.warning("Etiqueta não encontrada", extra={"id": id})
        return "Etiqueta não encontrada", 404

    
    modelo = request.args.get("modelo", "67x26")
    qtd = int(request.args.get("qtd", 1))

    logger.info(
        "Preparando impressão",
        extra={"modelo": modelo, "quantidade": qtd}
    )

    validade_br = formatar_data_br(item["validade"])

    zpl = gerar_zpl_por_modelo(
        modelo=modelo,
        codigo=item["Codigo"],
        descricao=item["Descricao"],
        lote=item["Lote"],
        validade=validade_br
    )

    
    zpl_total = zpl
    
    logger.info("Enviando ZPL para agente de impressão")

    sucesso = enviar_para_agente(zpl_total, qtd)

    if not sucesso:
        logger.error("Agente de impressão OFFLINE ou inacessível")
        return (
            "⚠️ Agente de impressão offline. "
            "Verifique se o Zebra Agent está em execução.",
            503
        )



    
    logger.info(
        "Impressão concluída com sucesso",
        extra={"id": id, "quantidade": qtd}
    )

    return "Etiqueta enviada para a impressora"



@print_bp.route("/imprimir-fila")
def imprimir_fila():
    import re

    modelo = request.args.get("modelo", "67x26")
    numeros_raw = request.args.get("numeros", "")

    numeros = re.findall(r"\d+", numeros_raw)
    if not numeros:
        return "Nenhum lote informado", 400

    lotes = [f"LIC'{n}" for n in numeros]

    conn = get_conn()
    cur = conn.cursor()

    placeholders = ",".join("%s" for _ in lotes)
    cur.execute(f"""
        SELECT "Codigo", "Descricao", "Lote", "Validade" as validade
        FROM {TABELA}
        WHERE "Lote" IN ({placeholders})
        ORDER BY "Lote"
    """, lotes)

    itens = cur.fetchall()
    conn.close()

    if not itens:
        return "Nenhum item encontrado", 404

    zpl_total = ""

    for item in itens:
        zpl = gerar_zpl_por_modelo(
            modelo=modelo,
            codigo=item["Codigo"],
            descricao=item["Descricao"],
            lote=item["Lote"],
            validade=formatar_data_br(item["validade"])
        )
        zpl_total += zpl + "\n"

    logger.info(
    "Enviando fila de impressão para agente",
    extra={"total": len(itens)}
)

    sucesso = enviar_para_agente(zpl_total)

    if not sucesso:
        logger.error("Agente de impressão OFFLINE ou inacessível (fila)")
        return (
            "⚠️ Agente de impressão offline. "
            "Não foi possível enviar a fila de etiquetas.",
            503
        )



    return f"Fila enviada com {len(itens)} etiquetas"
