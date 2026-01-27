"""
Rotas de API (JSON) - Versão SQLAlchemy.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.db.models import db, Item # Importamos o motor e o modelo
from backend.services.status import normalizar_status

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/importar-item", methods=["POST"])
def importar_item():
    data = request.get_json()
    if not data:
        return {"erro": "JSON inválido"}, 400

    try:
        # 1. Tratamento da data
        validade = None
        validade_raw = data.get("validade")
        if validade_raw:
            try:
                validade = datetime.strptime(validade_raw, "%d/%m/%Y").date()
            except ValueError:
                validade = None

        # 2. Lógica de UPSERT (Sincronização)
        # Procuramos se já existe um item com o mesmo Código e Lote
        item = Item.query.filter_by(Codigo=data["codigo"], Lote=data["lote"]).first()

        if item:
            # Se existe, atualizamos
            item.Descricao = data.get("descricao")
            item.Status = normalizar_status(data.get("status"))
            item.Validade = validade
        else:
            # Se não existe, criamos um novo
            novo_item = Item(
                Codigo=data["codigo"],
                Descricao=data.get("descricao"),
                Lote=data["lote"],
                Status=normalizar_status(data.get("status")),
                Validade=validade
            )
            db.session.add(novo_item)

        db.session.commit() # Grava no banco de dados
        return {"status": "ok"}

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}, 500


@api_bp.route("/api/importar-lote", methods=["POST"])
def importar_lote():
    data = request.get_json(silent=True)
    if not data or "itens" not in data:
        return {"erro": "JSON inválido ou chave 'itens' ausente"}, 400

    try:
        for item_data in data["itens"]:
            # Processamento de data
            validade = None
            v_raw = item_data.get("validade")
            if v_raw:
                try:
                    validade = datetime.strptime(v_raw, "%d/%m/%Y").date()
                except ValueError:
                    validade = None

            # UPSERT para cada item do lote
            item = Item.query.filter_by(
                Codigo=item_data["codigo"], 
                Lote=item_data["lote"]
            ).first()

            status_norm = normalizar_status(item_data.get("status"))

            if item:
                item.Descricao = item_data.get("descricao")
                item.Status = status_norm
                item.Validade = validade
            else:
                novo = Item(
                    Codigo=item_data["codigo"],
                    Descricao=item_data.get("descricao"),
                    Lote=item_data["lote"],
                    Status=status_norm,
                    Validade=validade
                )
                db.session.add(novo)

        db.session.commit() # Salva todos os itens de uma vez
        return {"status": "ok", "total_processado": len(data["itens"])}

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}, 500
    
    
@api_bp.route("/api/itens", methods=["GET"])
def listar_itens():
    try:
        # Busca os últimos 50 itens cadastrados para mostrar no monitor
        itens = Item.query.order_by(Item.id.desc()).limit(50).all()
        
        lista = []
        for i in itens:
            lista.append({
                "id": i.id,
                "codigo": i.Codigo,
                "descricao": i.Descricao,
                "lote": i.Lote,
                "validade": i.Validade.strftime("%d/%m/%Y") if i.Validade else None,
                "status": i.Status
            })
        return jsonify(lista)
    except Exception as e:
        return {"erro": str(e)}, 500  