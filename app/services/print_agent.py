import requests
from app.logger import logger
from app.config import Config # Importação está correta

def agente_online(timeout=5) -> bool:
    # ERRO ANTERIOR: Config.replace
    # CORREÇÃO: Usar o atributo AGENT_PRINT_URL
    health_url = Config.AGENT_PRINT_URL.replace("/print", "/health")

    try:
        r = requests.get(health_url, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException:
        return False


def enviar_para_agente(zpl: str, copies: int = 1) -> bool:
    payload = {
        "zpl": zpl,
        "copies": copies
    }

    try:
        # ERRO ANTERIOR: requests.post(Config, ...)
        # CORREÇÃO: Passar a URL que está dentro da classe
        response = requests.post(
            Config.AGENT_PRINT_URL, 
            json=payload,
            timeout=10
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
