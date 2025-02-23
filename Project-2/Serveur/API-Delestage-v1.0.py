from flask import Flask, request, jsonify
from flask_cors import CORS
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import requests
import json
import os
import time
import threading

app = Flask(__name__)
CORS(app)

# Initialisation des relais
relays = {}
serial_number = 369498  # Remplace par le numéro de série réel

for i in range(8):
    relay = DigitalOutput()
    relay.setDeviceSerialNumber(serial_number)
    relay.setChannel(i)
    
    try:
        relay.openWaitForAttachment(5000)
        time.sleep(0.5)
        if not relay.getAttached():
            raise PhidgetException(0x34)
        relay.setState(False)
        time.sleep(0.5)
        relays[i] = relay
        print(f"✅ Relais {i} attaché avec succès.")
    except PhidgetException as e:
        print(f"❌ Erreur d'attachement pour le relais {i}: {e}")

relay_states = {i: False for i in range(8)}

def passOn(num):
    if num in relays:
        relays[num].setState(True)
        relay_states[num] = True
        print(f"Relais {num} ON")

def passOff(num):
    if num in relays:
        relays[num].setState(False)
        relay_states[num] = False
        print(f"Relais {num} OFF")

@app.route('/toggle_relay', methods=['POST'])
def toggle_relay():
    data = request.json
    relay_id = int(data.get("relay"))
    state = bool(data.get("state"))
    
    if relay_id in relays:
        relays[relay_id].setState(state)
        relay_states[relay_id] = state
        return jsonify({"status": "success", "relay": relay_id, "state": state})
    
    return jsonify({"status": "error", "message": "Invalid relay"}), 400

# Gestion de la récupération des données Ecowatt
def get_oauth_token():
    url = "https://digital.iservices.rte-france.com/token/oauth"
    headers = {
        'Authorization': 'Basic OTRlMDkyZjctMjYyYS00NTIwLWFmYTctNDcwNGJlYjAwNjEyOjVmNjYyMTY1LWQ2MDctNGI3Ny1hNjYzLTc0Y2U0NzRlMDc1ZA==',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()['access_token']
    return None

def fetch_ecowatt_data():
    token = get_oauth_token()
    if not token:
        print("❌ Impossible de récupérer le token")
        return
    
    url = "https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        with open("ecowatt.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("✅ Données Ecowatt mises à jour")

def analyze_ecowatt_data():
    if not os.path.exists("ecowatt.json"):
        return
    
    with open("ecowatt.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for signal in data.get('signals', []):
        for entry in signal.get('values', []):
            if entry.get('hvalue') == 0:
                passOff(1)
            elif entry.get('hvalue') == 1:
                passOn(1)
    passOn(0)  # Toujours allumé

def periodic_task():
    while True:
        analyze_ecowatt_data()
        time.sleep(3600)  # Vérification toutes les 60 minutes

def api_update_task():
    while True:
        fetch_ecowatt_data()
        time.sleep(172800)  # Mise à jour tous les 2 jours

if __name__ == '__main__':
    threading.Thread(target=periodic_task, daemon=True).start()
    threading.Thread(target=api_update_task, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
