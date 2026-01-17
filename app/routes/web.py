"""
Rotas WEB (HTML).

Responsável por:
- renderizar templates
- busca de dados para exibição
- páginas da aplicação
"""



from flask import Blueprint, render_template, request
from app.db.models import db, Item  
from app.config import Config

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def home():
    return render_template("index.html", resultados=None)


@web_bp.route("/buscar")
def buscar():
    import re
    numeros_raw = request.args.get("numeros", "").strip()
    numeros = re.findall(r"\d+", numeros_raw)

    if not numeros:
        return render_template("index.html", resultados=None)

    
    lotes_formatados = [f"LIC'{n}" for n in numeros]

    
    resultados = Item.query.filter(Item.Lote.in_(lotes_formatados)).all()

    mensagem = None
    if not resultados:
        mensagem = f"⚠️ Nenhum lote encontrado para: {', '.join(lotes_formatados)}"

    return render_template(
        "index.html",
        resultados=resultados,
        numeros=numeros_raw,
        mensagem=mensagem
    )


@web_bp.route("/etiqueta/<int:id>")
def etiqueta(id):
    
    item = Item.query.get(id) 

    if not item:
        return "Etiqueta não encontrada", 404

    return render_template(
        "label.html",
        item_id=id,
        codigo=item.Codigo,      
        descricao=item.Descricao, 
        lote=item.Lote,           
        validade=item.Validade    
    )
