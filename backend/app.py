# backend/app.py
from flask import Flask
from flask_cors import CORS

# Adicione "backend." na frente de todos os seus módulos locais
from backend.config import Config 
from backend.routes.api import api_bp
from backend.routes.print import print_bp
from backend.logger import logger
from backend.db.models import db 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(api_bp)
app.register_blueprint(print_bp)

logger.info("Aplicação Flask iniciada (Modo Módulo)")