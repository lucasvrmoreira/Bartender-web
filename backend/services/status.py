"""
Serviço de status.

Responsável por:
- normalizar
- validar
- padronizar status de itens

Usado por APIs e importações.
"""


def normalizar_status(status):
    if not status:
        return "Liberado"

    s = str(status).strip().lower()

    if s == "liberado":
        return "Liberado"
    if s == "bloqueado":
        return "Bloqueado"
    if s in ("nao acessivel", "não acessível", "nao acessível"):
        return "Nao acessivel"

    return "Nao acessivel"
