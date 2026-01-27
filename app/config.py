"""
Arquivo de configuração da aplicação.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Ajuste para garantir que a URL funcione no SQLAlchemy síncrono
    uri = os.getenv("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    AGENT_PRINT_URL = os.getenv("AGENT_PRINT_URL", "http://127.0.0.1:9101/print")
    TABELA = "cellavita"
    SCHEMA = "barthenderweb"

# Mantendo as variáveis globais que seus outros arquivos já importam
AGENT_PRINT_URL = Config.AGENT_PRINT_URL
TABELA = Config.TABELA