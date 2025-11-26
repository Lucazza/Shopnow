from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

# Pega o ID do container ou usa um padrão
SERVER_ID = os.getenv('SERVER_ID', 'Unknown')

@app.route('/')
def home():
    # Simula um pequeno processamento
    return jsonify({
        "message": "Bem-vindo à ShopNow!",
        "server": SERVER_ID,
        "status": "active"
    })

@app.route('/health')
def health():
    # Endpoint para o LB checar se o servidor está vivo
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)