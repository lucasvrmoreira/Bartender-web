"""
Arquivo de bootstrap da aplicação Flask.

Responsabilidade:
- criar a instância do Flask
- registrar os blueprints (rotas)
"""



from flask import Flask

from app.routes.web import web_bp
from app.routes.api import api_bp
from app.routes.print import print_bp
from app.logger import logger

logger.info("Aplicação iniciada")

app = Flask(__name__)

app.register_blueprint(web_bp)
app.register_blueprint(api_bp)
app.register_blueprint(print_bp)
