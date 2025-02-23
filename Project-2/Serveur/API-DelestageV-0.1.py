from flask import Flask, request, jsonify
from flask_cors import CORS
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import time

app = Flask(__name__)
CORS(app)

# Initialisation des relais
relays = {}
relay_states = {i: False for i in range(8)}
serial_number = 317286  # Remplace par le numéro de série réel

for i in range(8):
    relay = DigitalOutput()
    relay.setDeviceSerialNumber(serial_number)
    relay.setChannel(i)

    try:
        relay.openWaitForAttachment(5000)  # Attente de connexion (5s max)
        time.sleep(0.5)  # Pause de 500ms

        if not relay.getAttached():  # Vérifie que le périphérique est bien attaché
            raise PhidgetException(0x34)  # Lève une exception si non attaché

        relay.setState(False)  # Éteint le relais au démarrage
        relay_states[i] = False  # Stocke l'état
        time.sleep(0.5)  # Pause pour éviter de spammer

        relays[i] = relay
        print(f"✅ Relais {i} attaché avec succès.")

    except PhidgetException as e:
        print(f"❌ Erreur d'attachement pour le relais {i}: {e}")

print("🟢 Initialisation terminée.")

def passOn(num):
    if num in relays and relays[num].getAttached():
        relays[num].setState(True)
        relay_states[num] = True
        print(f"Relais {num} ON")

def passOff(num):
    if num in relays and relays[num].getAttached():
        relays[num].setState(False)
        relay_states[num] = False
        print(f"Relais {num} OFF")

@app.route('/toggle_relay', methods=['POST'])
def toggle_relay():
    data = request.json
    relay_id = int(data.get("relay"))
    state = bool(data.get("state"))

    if relay_id in relays and relays[relay_id].getAttached():
        relays[relay_id].setState(state)
        relay_states[relay_id] = state
        return jsonify({"status": "success", "relay": relay_id, "state": state})
    
    return jsonify({"status": "error", "message": "Invalid or unattached relay"}), 400

@app.route('/get_relays_state', methods=['GET'])
def get_relays_state():
    return jsonify(relay_states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
