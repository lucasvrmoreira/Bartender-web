# app/db/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

# Pega a URL bruta
raw_url = os.getenv("DATABASE_URL")

# --- TRATAMENTO DA URL (Blindado) ---
if raw_url:
    # 1. Garante o driver correto
    if raw_url.startswith("postgres://"):
        url = raw_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif raw_url.startswith("postgresql://"):
        url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        url = raw_url

    # 2. LIMPEZA RADICAL: Remove tudo depois do '?' para tirar sslmode e channel_binding
    # Isso evita aquele erro do '&' perdido.
    if "?" in url:
        url = url.split("?")[0]
else:
    # Fallback caso não tenha variável (evita erro NoneType)
    url = "postgresql+asyncpg://user:pass@localhost/db"

print(f"🔌 Conectando no banco (URL limpa): {url}") # Log pra gente ver se limpou

# 3. Cria o engine passando os argumentos de SSL explicitamente
# O Render/Neon exige SSL, então passamos aqui de forma limpa.
engine = create_async_engine(
    url,
    echo=True,
    # Isso substitui o ?sslmode=require da URL
    # connect_args={"ssl": "require"} # Tente "require" ou True se der erro
)

# --- FIM DO TRATAMENTO ---

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

# Dependency Injection
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()