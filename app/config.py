"""
Arquivo de configuração da aplicação.

Responsável por:
- carregar variáveis de ambiente (.env)
- centralizar constantes globais (DATABASE_URL, TABELA, SCHEMA)

Usado por todo o projeto.
"""


import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    
    AGENT_PRINT_URL = os.getenv("AGENT_PRINT_URL", "http://127.0.0.1:9101/print")
    TABELA = "cellavita"
    SCHEMA = "barthenderweb"


AGENT_PRINT_URL = Config.AGENT_PRINT_URL
TABELA = Config.TABELA