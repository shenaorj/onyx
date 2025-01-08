from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir solicitudes desde el frontend

# Endpoint HTTP de QuickNode
http_endpoint = "YOUR_ENDPOINT"

@app.route("/analyze", methods=["POST"])
def analyze_wallet():
    data = request.get_json()
    wallet_address = data.get("walletAddress")
    
    if not wallet_address:
        return jsonify({"error": "No se proporcionó una dirección de wallet"}), 400

    # Consultar balance inicial
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [wallet_address]
    }
    
    try:
        response = requests.post(http_endpoint, json=payload)
        if response.status_code != 200:
            return jsonify({"error": f"Error del servidor: {response.status_code}"}), 500
        
        result = response.json()
        if "result" in result and "value" in result["result"]:
            balance_lamports = result["result"]["value"]
            balance_sol = balance_lamports / 1_000_000_000
            return jsonify({"balance": balance_sol})
        else:
            return jsonify({"error": "Respuesta inesperada del servidor"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)