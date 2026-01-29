"""
Factory de etiquetas.

Responsável por:
- escolher o modelo correto de etiqueta
- evitar if/else espalhado pelo código
"""

from backend.services.etiqueta.zpl_67x26 import gerar_zpl
from backend.services.etiqueta.zpl_40x20 import gerar_zpl_40x20
from backend.services.etiqueta.zpl_25x10 import gerar_zpl_25x10

# Adicionei 'com_qrcode=True' nos argumentos
def gerar_zpl_por_modelo(modelo, codigo, descricao, lote, validade, com_qrcode=True):
    if modelo == "40x20":
        # Modelos pequenos geralmente não cabem QR Code, então ignoramos o flag
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

    # Padrão (67x26) - AQUI repassamos a ordem do QR Code
    return gerar_zpl(
        codigo=codigo,
        descricao=descricao,
        lote=lote,
        validade=validade,
        com_qrcode=com_qrcode  # <--- O Factory agora avisa o ZPL
    )