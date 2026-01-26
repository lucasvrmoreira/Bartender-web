from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager
from app.db.database import get_db, engine, Base
from app.routers import items 
from app.routers import print as print_router
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware


# 1. LIFESPAN (Gerenciador de Vida)
# Inicia o banco quando o app liga
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FastAPI Iniciando...")
    # Opcional: Cria tabelas (bom para garantir que o banco ta conectado)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # CUIDADO!
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("🛑 FastAPI Encerrando...")

# 2. A CRIAÇÃO DO APP
app = FastAPI(
    title="Bartender API",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste conforme necessário para segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. ROTA DE TESTE (Health Check)
@app.get("/")
async def health_check():
    return {"status": "ok", "message": "O FastAPI está vivo e respirando! 🚀"}

# 4. ROTA DE TESTE DO BANCO (A Prova de Fogo)
@app.get("/db-test")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        # Executa uma query simples SQL
        result = await db.execute(text("SELECT 'Conexão Async Funcionando!'"))
        message = result.scalar()
        return {"db_status": "success", "message": message}
    except Exception as e:
        return {"db_status": "error", "error": str(e)}
    
@app.get("/db-test")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    # ... (seu código existente) ...
    pass 

# --- ADICIONE ISTO AQUI NO FINAL DO ARQUIVO ---
app.include_router(items.router)
app.include_router(print_router.router)