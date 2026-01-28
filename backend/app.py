# backend/app.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, jsonify
from flask_cors import CORS

# Adicione "backend." na frente de todos os seus módulos locais
from backend.config import Config 
from backend.routes.api import api_bp
from backend.routes.print import print_bp
from backend.logger import logger
from backend.db.models import db 

# --- CONFIGURAÇÃO SENTRY (BACKEND NUVEM) ---
sentry_sdk.init(
    # Usando o mesmo DSN para centralizar tudo no mesmo painel
    dsn="https://4bd9fd38a43bc12e40657228cec7ecb3@o4510788220092416.ingest.us.sentry.io/4510788226711552",
    
    integrations=[FlaskIntegration()],
    
    # Monitora 100% das transações (útil para ver lentidão no banco/api)
    traces_sample_rate=1.0,
    
    # O PULO DO GATO: Nomeamos diferente do agente local
    # Assim você sabe: "Isso é erro do Servidor Render" vs "Isso é erro do PC Local"
    environment="backend-render"
)
# -------------------------------------------

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(api_bp)
app.register_blueprint(print_bp)

# Rota Opcional: Só para você testar se o Backend está enviando erros
@app.route("/debug-sentry-backend")
def debug_sentry():
    raise Exception("Teste de Erro no Backend Render!")

logger.info("Aplicação Flask iniciada (Modo Módulo)")