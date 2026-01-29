"""
Rotas de impressão.

Responsável por:
- buscar dados no banco
- gerar etiquetas (via factory)
- enviar ZPL para a impressora Zebra
"""

from flask import Blueprint, request
from backend.logger import logger
from backend.db.models import db, Item
from backend.utils.datas import formatar_data_br
from backend.services.etiqueta.factory import gerar_zpl_por_modelo
from backend.services.print_agent import enviar_para_agente


print_bp = Blueprint("print", __name__)


@print_bp.route("/api/imprimir/<int:id>")
def imprimir_etiqueta(id):
    
    logger.info("Solicitação de impressão", extra={"id": id})

    item = db.session.query(Item).get(id)
    
    if not item:
        logger.warning("Etiqueta não encontrada", extra={"id": id})
        return "Etiqueta não encontrada", 404
    
    modelo = request.args.get("modelo", "67x26")
    qtd = int(request.args.get("qtd", 1))

    # --- NOVIDADE: Ler o status do QR Code da URL ---
    # Se vier "true", vira True. Se vier "false", vira False.
    qrcode_param = request.args.get("qrcode", "true") 
    com_qrcode = qrcode_param.lower() == "true"

    logger.info(
        "Preparando impressão",
        extra={"modelo": modelo, "quantidade": qtd, "qrcode": com_qrcode}
    )

    validade_br = formatar_data_br(item.Validade)

    zpl = gerar_zpl_por_modelo(
        modelo=modelo,
        codigo=item.Codigo,
        descricao=item.Descricao,
        lote=item.Lote,
        validade=validade_br,
        com_qrcode=com_qrcode # <--- Passamos a decisão para a Factory
    )
    
    logger.info("Enviando ZPL para agente de impressão")

    sucesso = enviar_para_agente(zpl, qtd)

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


@print_bp.route("/api/imprimir-fila")
def imprimir_fila():
    import re

    modelo = request.args.get("modelo", "67x26")
    numeros_raw = request.args.get("numeros", "")
    
    # Na fila, por enquanto, deixamos o QR Code como padrão (True)
    # ou você pode ler da URL também se quiser.
    qrcode_param = request.args.get("qrcode", "true")
    com_qrcode = qrcode_param.lower() == "true"

    numeros = re.findall(r"\d+", numeros_raw)
    if not numeros:
        return "Nenhum lote informado", 400

    lotes = [f"LIC'{n}" for n in numeros]

    itens = Item.query.filter(Item.Lote.in_(lotes)).all()

    if not itens:
        return "Nenhum item encontrado", 404

    zpl_total = ""

    for item in itens:
        zpl = gerar_zpl_por_modelo(
            modelo=modelo,
            codigo=item.Codigo,
            descricao=item.Descricao,
            lote=item.Lote,
            validade=formatar_data_br(item.Validade),
            com_qrcode=com_qrcode # Também aplicamos na fila
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