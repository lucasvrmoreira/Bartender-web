"""
Rotas WEB (HTML).

Responsável por:
- renderizar templates
- busca de dados para exibição
- páginas da aplicação
"""



from flask import Blueprint, render_template, request

from app.db.connection import get_conn
from app.config import TABELA

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

    lotes = [f"LIC'{n}" for n in numeros]

    conn = get_conn()
    cur = conn.cursor()

    if len(lotes) == 1:
        cur.execute(f"""
            SELECT id, "Codigo", "Descricao", "Lote", "Validade" as validade
            FROM {TABELA}
            WHERE "Lote" LIKE %s
            ORDER BY "Lote"
            LIMIT 50
        """, (lotes[0] + "%",))
    else:
        placeholders = ",".join("%s" for _ in lotes)
        cur.execute(f"""
            SELECT id, "Codigo", "Descricao", "Lote", "Validade" as validade
            FROM {TABELA}
            WHERE "Lote" IN ({placeholders})
            ORDER BY "Lote"
        """, lotes)

    resultados = cur.fetchall()
    conn.close()

    mensagem = None
    if not resultados:
        mensagem = "⚠️ Nenhum lote encontrado para a busca informada."

    return render_template(
        "index.html",
        resultados=resultados,
        numeros=numeros_raw,
        mensagem=mensagem
    )


@web_bp.route("/etiqueta/<int:id>")
def etiqueta(id):
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
        return "Etiqueta não encontrada", 404

    return render_template(
        "label.html",
        item_id=id,
        codigo=item["Codigo"],
        descricao=item["Descricao"],
        lote=item["Lote"],
        validade=item["validade"]
    )
