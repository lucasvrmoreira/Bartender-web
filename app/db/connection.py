from flask_sqlalchemy import SQLAlchemy
from app.config import DATABASE_URL
import os   

def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', DATABASE_URL)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if os.getenv("APP_ENV") == "production":
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"sslmode": "require"}}
        
    
    from app.db.models import db
    db.init_app(app)
