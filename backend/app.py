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
    
    # Monitora 100% das transações 
    traces_sample_rate=1.0,
    
    
    environment="backend-render"
)
# -------------------------------------------

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(api_bp)
app.register_blueprint(print_bp)


