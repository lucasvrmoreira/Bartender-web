"""
Factory de etiquetas.

Responsável por:
- escolher o modelo correto de etiqueta
- evitar if/else espalhado pelo código
"""



from app.services.etiqueta.zpl_67x26 import gerar_zpl
from app.services.etiqueta.zpl_40x20 import gerar_zpl_40x20
from app.services.etiqueta.zpl_25x10 import gerar_zpl_25x10


def gerar_zpl_por_modelo(modelo, codigo, descricao, lote, validade):
    if modelo == "40x20":
        return gerar_zpl_40x20(
            codigo=codigo,
            descricao=descricao,
            lote=lote,
            validade=validade
        )

    if modelo == "25x10":
        return gerar_zpl_25x10(
            codigo=codigo,
            descricao=descricao,
            lote=lote,
            validade=validade
        )

    # padrão
    return gerar_zpl(
        codigo=codigo,
        descricao=descricao,
        lote=lote,
        validade=validade
    )
