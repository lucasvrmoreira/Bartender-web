from flask import Blueprint, request, jsonify
from datetime import datetime
import re 
from sqlalchemy import or_, and_

from backend.db.models import db, Item
from backend.services.status import normalizar_status

api_bp = Blueprint("api", __name__)

# Função para converter data (Princípio DRY - Não repita a si mesmo)
def converter_data(data_raw):
    """Tenta converter a string de data, retorna None se falhar ou vier vazio."""
    if not data_raw:
        return None
    try:
        return datetime.strptime(data_raw, "%d/%m/%Y").date()
    except ValueError:
        return None


@api_bp.route("/api/importar-item", methods=["POST"])
def importar_item():
    data = request.get_json()
    if not data:
        return {"erro": "JSON inválido"}, 400

    # Prevenção de KeyError 
    codigo = data.get("codigo")
    lote = data.get("lote")
    
    # Validação: Se o usuário não mandou a moeda (código e lote), a máquina avisa e para aqui.
    if not codigo or not lote:
        return {"erro": "Os campos 'codigo' e 'lote' são obrigatórios."}, 400

    try:
        
        validade = converter_data(data.get("validade"))

        item = Item.query.filter_by(Codigo=codigo, Lote=lote).first()

        if item:
            item.Descricao = data.get("descricao")
            item.Status = normalizar_status(data.get("status"))
            item.Validade = validade
        else:
            novo_item = Item(
                Codigo=codigo,
                Descricao=data.get("descricao"),
                Lote=lote,
                Status=normalizar_status(data.get("status")),
                Validade=validade
            )
            db.session.add(novo_item)

        db.session.commit()
        return {"status": "ok"}

    except Exception as e:
        db.session.rollback()
        #  Segurança: Escondemos o erro real do usuário, mas registramos para nós mesmos.
        print(f"ERRO CRÍTICO na rota importar-item: {e}") # Em produção, usaríamos uma biblioteca de logs
        return {"erro": "Falha interna no servidor ao processar o item."}, 500


@api_bp.route("/api/importar-lote", methods=["POST"])
def importar_lote():
    data = request.get_json(silent=True)
    if not data or "itens" not in data:
        return {"erro": "JSON inválido ou chave 'itens' ausente"}, 400

    itens_recebidos = data["itens"]
    if not itens_recebidos:
        return {"status": "ok", "total_processado": 0}

    try:
        #  Criamos uma lista de condições para buscar TODOS os itens de uma vez só no banco, usando OR entre eles.
        condicoes = []
        for item in itens_recebidos:
            cod = item.get("codigo")
            lote = item.get("lote")
            if cod and lote:
                # Cria a condição: (Codigo == cod E Lote == lote)
                condicoes.append(and_(Item.Codigo == cod, Item.Lote == lote))

        # Fazemos UMA ÚNICA busca no banco de dados! 
        # Trazemos todos os itens que deram "Match" nas condições acima.
        itens_existentes = []
        if condicoes:
            itens_existentes = Item.query.filter(or_(*condicoes)).all()

        # MAPA DE MEMÓRIA (Dicionário): A chave é (Codigo, Lote) e o valor é o Item do banco
        mapa_itens = {(i.Codigo, i.Lote): i for i in itens_existentes}

        novos_itens = []

        # 2. Agora, para cada item recebido, verificamos se ele já existe no mapa.
        for item_data in itens_recebidos:
            cod = item_data.get("codigo")
            lote = item_data.get("lote")
            
            if not cod or not lote:
                continue # Ignora itens que vieram sem código ou lote por segurança

            # Utilizamos a função de conversão de data para garantir que a validade esteja no formato correto ou seja None.
            validade = converter_data(item_data.get("validade"))
            status_norm = normalizar_status(item_data.get("status"))

            # Procuramos o item no mapa usando a chave (Codigo, Lote)
            item_bd = mapa_itens.get((cod, lote))

            if item_bd:
                # Se existe no mapa, apenas atualizamos
                item_bd.Descricao = item_data.get("descricao")
                item_bd.Status = status_norm
                item_bd.Validade = validade
            else:
                # Se não existe, preparamos um novo
                novo = Item(
                    Codigo=cod,
                    Descricao=item_data.get("descricao"),
                    Lote=lote,
                    Status=status_norm,
                    Validade=validade
                )
                novos_itens.append(novo)

        #  Adicionamos todos os novos de uma vez só no banco
        if novos_itens:
            db.session.add_all(novos_itens)

        # O commit finaliza a transação, seja para atualizar os existentes ou adicionar os novos.
        db.session.commit()
        return {"status": "ok", "total_processado": len(itens_recebidos)}

    except Exception as e:
        db.session.rollback()
        # Log escondido do usuário
        print(f"ERRO CRÍTICO na rota importar-lote: {e}")
        return {"erro": "Falha interna ao processar o lote de itens."}, 500
    
    
PREFIXO_LOTE = "LIC'"

@api_bp.route("/api/itens", methods=["GET"])
def listar_itens():
    try:
        # Busca os últimos 50 itens cadastrados para mostrar no monitor
        itens = Item.query.order_by(Item.id.desc()).limit(50).all()
        
        # Transformamos os objetos do banco em dicionários para enviar como JSON.
        lista = [{
            "id": i.id,
            "codigo": i.Codigo,
            "descricao": i.Descricao,
            "lote": i.Lote,
            "validade": i.Validade.strftime("%d/%m/%Y") if i.Validade else None,
            "status": i.Status
        } for i in itens]

        return jsonify(lista)

    except Exception as e:
        # Escondemos o erro do cliente e guardamos para nós
        print(f"ERRO CRÍTICO na rota listar-itens: {e}")
        return {"erro": "Falha interna ao buscar a lista de itens."}, 500
    
    
@api_bp.route("/api/buscar", methods=["GET"])
def buscar_lotes():
    numeros_raw = request.args.get("lotes", "").strip()
    if not numeros_raw:
        return jsonify([])

    # Extraímos apenas os números da string que o usuário enviou
    numeros = re.findall(r"\d+", numeros_raw)
    
    # Usamos a nossa constante em vez de escrever "LIC'" direto no código
    lotes_formatados = [f"{PREFIXO_LOTE}{n}" for n in numeros]

    try:
        resultados = Item.query.filter(Item.Lote.in_(lotes_formatados)).all()
        
        lista = [{
            "id": i.id,
            "codigo": i.Codigo,
            "descricao": i.Descricao,
            "lote": i.Lote,
            "validade": i.Validade.strftime("%d/%m/%Y") if i.Validade else None
        } for i in resultados]
        
        return jsonify(lista)

    except Exception as e:
        print(f"ERRO CRÍTICO na rota buscar-lotes: {e}")
        return jsonify({"erro": "Falha interna ao realizar a busca de lotes."}), 500