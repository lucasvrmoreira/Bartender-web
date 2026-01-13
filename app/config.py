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

DATABASE_URL = os.getenv("DATABASE_URL")
AGENT_PRINT_URL = os.getenv("AGENT_PRINT_URL")


TABELA = "cellavita"
SCHEMA = "barthenderweb"
