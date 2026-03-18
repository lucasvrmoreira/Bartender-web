
import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def obter_url_banco() -> str:
    """Busca e higieniza a URL do banco de dados de forma segura."""
    raw_url = os.getenv("DATABASE_URL")
    
    # FAIL FAST: Se não tem URL, a API não pode nem ligar.
    if not raw_url:
        raise ValueError("CRÍTICO: A variável DATABASE_URL não foi encontrada no .env ou no servidor!")

    url = raw_url
    
    # Corrige o driver para AsyncPG (Padrão para Render/Neon/Heroku)
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Limpeza radical de parâmetros conflitantes do asyncpg
    if "?" in url:
        url = url.split("?")[0]
        
    return url

DATABASE_URL = obter_url_banco()

# Log Seguro: Mostra que conectou, mas esconde a senha
logger.info("🔌 Configurando conexão com o banco de dados (Credenciais ocultas)")

# Engine Dinâmica: echo=True SÓ no seu PC, nunca em produção
ambiente = os.getenv("ENVIRONMENT", "development")
is_dev = ambiente == "development"

engine = create_async_engine(
    DATABASE_URL,
    echo=is_dev, 
    # DICA PARA O RENDER/NEON: Se der erro de SSL lá na nuvem, 
    # descomente a linha abaixo apenas no ambiente de produção:
    # connect_args={"ssl": "require"} if not is_dev else {}
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# SQLAlchemy Base para os modelos
class Base(DeclarativeBase):
    pass

# Dependency Injection para o FastAPI
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()