"""
Arquivo de bootstrap da aplicação Flask.

Responsabilidade:
- criar a instância do Flask
- registrar os blueprints (rotas)
"""



from flask import Flask
from backend.config import Config
from backend.routes.web import web_bp
from backend.routes.api import api_bp
from backend.routes.print import print_bp
from backend.logger import logger
from flask_cors import CORS


# Importa o andaime
from backend.db.models import db 

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(web_bp)
app.register_blueprint(api_bp)
app.register_blueprint(print_bp)

logger.info("Aplicação iniciada com Banco de Dados")