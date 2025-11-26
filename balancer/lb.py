import requests
import random
from flask import Flask, request, jsonify
from itertools import cycle

app = Flask(__name__)

# Lista das instâncias (nomes definidos no docker-compose)
SERVERS = ["http://shop-1:5000", "http://shop-2:5000", "http://shop-3:5000"]

# Iterador para o Round Robin
server_pool = cycle(SERVERS)

def is_healthy(url):
    """Verifica se o servidor está respondendo antes de enviar tráfego."""
    try:
        response = requests.get(f"{url}/health", timeout=1)
        return response.status_code == 200
    except:
        return False

def get_server_round_robin():
    """Algoritmo 1: Round Robin (Circular)"""
    # Tenta encontrar um servidor saudável no ciclo
    for _ in range(len(SERVERS)):
        server = next(server_pool)
        if is_healthy(server):
            return server
    return None

def get_server_random():
    """Algoritmo 2: Random (Aleatório)"""
    # Filtra apenas os servidores saudáveis
    healthy_servers = [s for s in SERVERS if is_healthy(s)]
    if healthy_servers:
        return random.choice(healthy_servers)
    return None

@app.route('/')
def proxy():
    # Mude aqui para testar o outro algoritmo: get_server_random()
    target_server = get_server_round_robin() 
    
    if not target_server:
        return jsonify({"error": "Nenhum servidor disponível!"}), 503

    try:
        # Repassa a requisição para o servidor escolhido
        response = requests.get(target_server)
        return response.content, response.status_code, response.headers.items()
    except:
        return jsonify({"error": "Falha ao conectar ao servidor"}), 500

if __name__ == "__main__":
    print("Balanceador ShopNow iniciado na porta 8080...")
    app.run(host='0.0.0.0', port=8080)