"""
Utilitários de data.

Responsável por:
- formatação de datas
- conversões simples
"""


def formatar_data_br(data):
    if not data:
        return ""
    try:
        return data.strftime("%d/%m/%Y")
    except Exception:
        return str(data)
