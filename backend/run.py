"""
Arquivo de entrada da aplicação.
Responsável apenas por iniciar o servidor Flask.
"""


import os
from dotenv import load_dotenv

load_dotenv()

print("DATABASE_URL LIDA PELO PYTHON:", os.getenv("DATABASE_URL"))

from backend.app import app

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=False,
        use_reloader=False  
        
        
        )
