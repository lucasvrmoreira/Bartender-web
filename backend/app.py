# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importaremos as rotas que vamos criar no Passo 2
from backend.routes.api import router as api_router
from backend.routes.print import router as print_router

# Inicializa o FastAPI (Substitui o app = Flask(__name__))
app = FastAPI(title="API Cellavita", description="Migração para FastAPI", version="1.0.0")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, troque "*" pelos domínios reais do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas (Substitui o app.register_blueprint)
app.include_router(api_router)
app.include_router(print_router)

# Rota raiz de teste para saber se a API subiu
@app.get("/")
async def root():
    return {"mensagem": "API Cellavita está rodando no FastAPI com AsyncPG!"}