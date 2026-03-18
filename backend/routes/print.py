"""
Rotas de impressão (Refatorado).
"""
import re 
from flask import Blueprint, request, jsonify
from backend.logger import logger
from backend.db.models import db, Item
from backend.utils.datas import formatar_data_br
from backend.services.etiqueta.factory import gerar_zpl_por_modelo
from backend.services.print_agent import enviar_para_agente

print_bp = Blueprint("print", __name__)


# O ideal seria importar isso de um arquivo 'config.py', mas deixamos aqui para facilitar.
PREFIXO_LOTE = "LIC'"

# Função para garantir que a quantidade seja um número inteiro válido, sem quebrar o sistema.
def obter_quantidade_segura(valor_raw, padrao=1):
    """Garante que a quantidade será um número inteiro válido, sem quebrar o sistema."""
    try:
        if valor_raw:
            return int(valor_raw)
    except ValueError:
        logger.warning(f"Tentativa de converter quantidade inválida: {valor_raw}. Usando padrão {padrao}.")
    return padrao


@print_bp.route("/api/imprimir/<int:id>")
def imprimir_etiqueta(id):
    logger.info("Solicitação de impressão", extra={"id": id})

    try:
        #  Busca no Banco de Dados
        item = db.session.query(Item).get(id)
        if not item:
            logger.warning("Etiqueta não encontrada", extra={"id": id})
            return jsonify({"erro": "Etiqueta não encontrada"}), 404
        
        # Leitura e Validação de Parâmetros
        modelo = request.args.get("modelo", "67x26")
        
        # Usamos a função segura em vez de int() direto
        qtd_raw = request.args.get("qtd")
        qtd = obter_quantidade_segura(qtd_raw, padrao=1)

        qrcode_param = request.args.get("qrcode", "true") 
        com_qrcode = qrcode_param.lower() == "true"

        logger.info("Preparando impressão", extra={"modelo": modelo, "quantidade": qtd, "qrcode": com_qrcode})

        # Gerar ZPL
        validade_br = formatar_data_br(item.Validade)
        zpl = gerar_zpl_por_modelo(
            modelo=modelo,
            codigo=item.Codigo,
            descricao=item.Descricao,
            lote=item.Lote,
            validade=validade_br,
            com_qrcode=com_qrcode
        )
        
        # Envio para a Impressora
        logger.info("Enviando ZPL para agente de impressão")
        sucesso = enviar_para_agente(zpl, qtd)

        if not sucesso:
            logger.error("Agente de impressão OFFLINE ou inacessível")
            return jsonify({"erro": "Agente de impressão offline. Verifique o Zebra Agent."}), 503
        
        logger.info("Impressão concluída com sucesso", extra={"id": id, "quantidade": qtd})
        
        return jsonify({"mensagem": "Etiqueta enviada para a impressora", "quantidade": qtd}), 200

    except Exception as e:
        logger.error(f"Erro crítico na impressão individual: {e}")
        return jsonify({"erro": "Falha interna ao processar a impressão."}), 500


@print_bp.route("/api/imprimir-fila")
def imprimir_fila():
    try:
        modelo = request.args.get("modelo", "67x26")
        numeros_raw = request.args.get("numeros", "")
        
        qrcode_param = request.args.get("qrcode", "true")
        com_qrcode = qrcode_param.lower() == "true"

        numeros = re.findall(r"\d+", numeros_raw)
        if not numeros:
            return jsonify({"erro": "Nenhum lote válido informado na URL"}), 400

        # Usando a constante em vez de código chumbado
        lotes = [f"{PREFIXO_LOTE}{n}" for n in numeros]

        # Busca protegida pelo try/except
        itens = Item.query.filter(Item.Lote.in_(lotes)).all()

        if not itens:
            return jsonify({"erro": "Nenhum item encontrado para os lotes informados"}), 404

        zpl_total = ""
        for item in itens:
            zpl = gerar_zpl_por_modelo(
                modelo=modelo,
                codigo=item.Codigo,
                descricao=item.Descricao,
                lote=item.Lote,
                validade=formatar_data_br(item.Validade),
                com_qrcode=com_qrcode
            )
            zpl_total += zpl + "\n"

        logger.info("Enviando fila de impressão", extra={"total": len(itens)})
        sucesso = enviar_para_agente(zpl_total)

        if not sucesso:
            logger.error("Agente de impressão OFFLINE (fila)")
            return jsonify({"erro": "Agente de impressão offline. Não foi possível enviar a fila."}), 503

        return jsonify({"mensagem": f"Fila enviada com {len(itens)} etiquetas"}), 200

    except Exception as e:
        logger.error(f"Erro crítico na fila de impressão: {e}")
        return jsonify({"erro": "Falha interna ao processar a fila de impressão."}), 500