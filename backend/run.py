import os
from dotenv import load_dotenv

load_dotenv()


from backend.app import app

@app.route('/')
def home():
    return {"message": "Backend rodando com sucesso!", "status": "online"}

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=True, # Mudei para True para te ajudar a ver erros se surgirem
        use_reloader=True
    )