import requests
from backend.logger import logger
from backend.config import Config

def agente_online(timeout=5) -> bool:
    # Garante que a URL de health esteja correta baseada na URL configurada
    base_url = Config.AGENT_PRINT_URL.replace("/print", "")
    health_url = f"{base_url}/health"
    
    try:
        r = requests.get(health_url, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException:
        return False

def enviar_para_agente(zpl: str, copies: int = 1) -> bool:
    url = Config.AGENT_PRINT_URL
    
    # 1. MUDANÇA IMPORTANTE: Enviamos 'copies' na URL (Query String)
    # Isso separa os dados da etiqueta das configurações de impressão
    params = {"copies": copies}
    
    try:
        # 2. O SEGREDO: Converter para Bytes UTF-8
        # Ao converter manualmente, garantimos que 'Á' continue 'Á' (byte C3 81)
        zpl_bytes = zpl.encode('utf-8')

        # 3. Enviar como RAW DATA (Bytes)
        # Usamos data=... em vez de json=...
        # Content-Type avisa o agente que está chegando um fluxo de bytes puro
        response = requests.post(
            url, 
            params=params,
            data=zpl_bytes, 
            headers={"Content-Type": "application/octet-stream"},
            timeout=10
        )
        response.raise_for_status()

        logger.info("Agente confirmou impressão")
        return True

    except requests.RequestException as e:
        logger.error(f"Falha ao enviar para o agente: {str(e)}")
        return False