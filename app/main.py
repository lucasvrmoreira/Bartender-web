# ARQUIVO: app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.database import engine, Base
# Importa suas rotas (incluindo o sync que criamos por último)
from app.routers import items, print as print_router, web, sync

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FastAPI Iniciando...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("🛑 FastAPI Encerrando...")

app = FastAPI(
    title="Bartender API",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AQUI ESTÁ A CORREÇÃO DOS CAMINHOS ---
# Isso conecta a URL /static com a pasta física app/static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rotas
app.include_router(items.router)
app.include_router(print_router.router)
app.include_router(web.router)
app.include_router(sync.router)