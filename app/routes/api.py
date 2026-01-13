"""
Rotas de API (JSON).

Responsável por:
- receber dados externos
- integrar com outros sistemas
- importar informações para o backend
"""


from flask import Blueprint, request
from datetime import datetime

from app.services.status import normalizar_status
from app.db.repository import upsert_item

api_bp = Blueprint("api", __name__)


@api_bp.route("/api/importar-item", methods=["POST"])
def importar_item():
    data = request.get_json()

    if not data:
        return {"erro": "JSON inválido"}, 400

    try:
        status = normalizar_status(data.get("status"))

        validade = None
        validade_raw = data.get("validade")
        if validade_raw:
            try:
                validade = datetime.strptime(validade_raw, "%d/%m/%Y").date()
            except ValueError:
                validade = None

        upsert_item(
            codigo=data["codigo"],
            descricao=data["descricao"],
            lote=data["lote"],
            status=status,
            validade=validade
        )
    except KeyError as e:
        return {"erro": f"Campo ausente: {str(e)}"}, 400
    except Exception as e:
        return {"erro": str(e)}, 500

    return {"status": "ok"}


@api_bp.route("/api/importar-lote", methods=["POST"])
def importar_lote():
    data = request.get_json(silent=True)

    if not data or "itens" not in data:
        return {"erro": "JSON inválido ou chave 'itens' ausente"}, 400

    total = 0

    try:
        for item in data["itens"]:
            status = normalizar_status(item.get("status"))

            validade = None
            validade_raw = item.get("validade")
            if validade_raw:
                try:
                    validade = datetime.strptime(validade_raw, "%d/%m/%Y").date()
                except ValueError:
                    validade = None

            upsert_item(
                codigo=item["codigo"],
                descricao=item["descricao"],
                lote=item["lote"],
                status=status,
                validade=validade
            )
            total += 1

    except KeyError as e:
        return {"erro": f"Campo ausente: {str(e)}"}, 400
    except Exception as e:
        return {"erro": str(e)}, 500

    return {"status": "ok", "total_processado": total}
