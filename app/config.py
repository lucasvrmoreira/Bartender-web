"""
Arquivo de configuração da aplicação.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # Testa se a conexão está viva antes de usar
        "pool_recycle": 300,    # Renova a conexão a cada 5 minutos
    }

    
    AGENT_PRINT_URL = os.getenv("AGENT_PRINT_URL", "http://127.0.0.1:9101/print")
    TABELA = "cellavita"
    SCHEMA = "barthenderweb"


AGENT_PRINT_URL = Config.AGENT_PRINT_URL
TABELA = Config.TABELA