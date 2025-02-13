import os
import requests
from flask import Flask, jsonify, request
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Paramètres de configuration Keycloak
KEYCLOAK_URL = "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token"
CLIENT_ID = "abra"
CLIENT_SECRET = "qc3c05GiFknf1io0vAOAsOETpgGdOkSD"
SCOPE = "psyko"

# Variable globale pour maintenir le compteur
counter = 0

# Fonction pour obtenir le token d'accès
def get_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPE  # Retirer si non nécessaire
    }
    
    response = requests.post(KEYCLOAK_URL, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Erreur lors de l'obtention du token : {response.text} (Code: {response.status_code})")

# Vérification de l'authentification OAuth2 via l'introspection du token
def verify_token(token):
    introspect_url = f"http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token/introspect"
    response = requests.post(introspect_url, data={
        'token': token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    
    if response.status_code == 200:
        # On retourne True si le token est actif
        return response.json().get("active", False)
    else:
        # Si l'introspection échoue, on retourne False
        return False

@app.route('/counter', methods=['GET'])
def api():
    global counter  # Utilisation de la variable globale counter

    # Récupérer le token depuis l'en-tête Authorization
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    # Extraire le token du header (Format: Bearer <token>)
    token = auth_header.split(" ")[1] if len(auth_header.split()) == 2 else None
    
    if not token:
        return jsonify({"error": "Token missing in Authorization header"}), 401
    
    try:
        # Vérifier le token
        if not verify_token(token):
            return jsonify({"error": "Invalid token"}), 401

        # Si le token est valide, incrémenter le compteur et renvoyer le résultat
        counter += 1
        return jsonify({"result": counter})

    except Exception as e:
        # Si une erreur survient lors de la vérification du token
        return jsonify({"error": str(e)}), 401


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
