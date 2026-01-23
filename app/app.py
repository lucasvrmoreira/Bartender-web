"""
Arquivo de bootstrap da aplicação Flask.

Responsabilidade:
- criar a instância do Flask
- registrar os blueprints (rotas)
"""



from flask import Flask
from app.config import Config
from app.routes.web import web_bp
from app.routes.api import api_bp
from app.routes.print import print_bp
from app.logger import logger

# Importa o andaime
from app.db.models import db 

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(web_bp)
app.register_blueprint(api_bp)
app.register_blueprint(print_bp)

logger.info("Aplicação iniciada com Banco de Dados")