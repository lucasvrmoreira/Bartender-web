import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. PEGA A URL DO AMBIENTE
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. AJUSTA A URL PARA O ASYNCPG (SE FOR POSTGRES)
if DATABASE_URL:
    
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
        
    elif DATABASE_URL.startswith("postgresql://") and "asyncpg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 3. CRIA O MOTOR (ENGINE)
engine = create_async_engine(DATABASE_URL, echo=True)

# 4. FÁBRICA DE SESSÕES
# expire_on_commit=False é obrigatório no modo async
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 5. BASE DOS MODELS (Substitui o db.Model do Flask)
Base = declarative_base()

# 6. A DEPENDÊNCIA (O "Garçom")
# O FastAPI vai usar isso para entregar o banco para as rotas
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()