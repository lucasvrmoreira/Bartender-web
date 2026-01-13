import requests
from app.logger import logger
from app.config import AGENT_PRINT_URL


def agente_online(timeout=2) -> bool:
    health_url = AGENT_PRINT_URL.replace("/print", "/health")

    try:
        r = requests.get(health_url, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException:
        return False


def enviar_para_agente(zpl: str, copies: int = 1) -> bool:
    if not agente_online():
        logger.warning("Agente de impressão OFFLINE")
        return False

    payload = {
        "zpl": zpl,
        "copies": copies
    }

    logger.debug(
        "Enviando ZPL para agente de impressão",
        extra={"copies": copies}
    )

    try:
        response = requests.post(
            AGENT_PRINT_URL,
            json=payload,
            timeout=5
        )
        response.raise_for_status()

        logger.info("Agente confirmou impressão")
        return True

    except requests.RequestException:
        logger.error(
            "Falha ao comunicar com agente de impressão",
            exc_info=True
        )
        return False
