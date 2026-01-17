"""
Arquivo de bootstrap da aplicação Flask.

Responsabilidade:
- criar a instância do Flask
- registrar os blueprints (rotas)
"""



from flask import Flask
from app.db.models import db # Importa o db do seu models.py
from app.config import Config
from app.routes.web import web_bp
from app.routes.api import api_bp
from app.routes.print import print_bp
from app.logger import logger

app = Flask(__name__)
# 1. Carrega as configurações da classe Config
app.config.from_object(Config)

# 2. ESTA LINHA É A SOLUÇÃO: Conecta o SQLAlchemy ao Flask
db.init_app(app)

app.register_blueprint(web_bp)
app.register_blueprint(api_bp)
app.register_blueprint(print_bp)

logger.info("Aplicação iniciada com Banco de Dados")