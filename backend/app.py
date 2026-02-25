from flask import Flask
from flask_cors import CORS
from backend.config import Config 
from backend.routes.api import api_bp
from backend.routes.print import print_bp
from backend.db.models import db 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

# Inicialização do DB
db.init_app(app)

# Registre as rotas
app.register_blueprint(api_bp)
app.register_blueprint(print_bp)