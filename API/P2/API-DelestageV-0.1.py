from flask import Flask, request, jsonify
from flask_cors import CORS
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *

app = Flask(__name__)
CORS(app)

# Initialisation des relais
relays = {}
serial_number = 369498  # Remplace par le numéro de série réel

import time
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *

# Initialisation des relais
relays = {}
serial_number = 369498  # Remplace par ton numéro de série réel

for i in range(8):
    relay = DigitalOutput()
    relay.setDeviceSerialNumber(serial_number)
    relay.setChannel(i)

    try:
        relay.openWaitForAttachment(5000)  # Attente de connexion (5s max)
        time.sleep(0.5)  # Pause de 500ms pour éviter d'aller trop vite

        if not relay.getAttached():  # Vérifie que le périphérique est bien attaché
            raise PhidgetException(0x34)  # Lève une exception si non attaché

        relay.setState(False)  # Éteint le relais au démarrage
        time.sleep(0.5)  # Encore une pause pour éviter de spammer

        relays[i] = relay
        print(f"✅ Relais {i} attaché avec succès.")

    except PhidgetException as e:
        print(f"❌ Erreur d'attachement pour le relais {i}: {e}")

print("🟢 Initialisation terminée.")

# Stocker l'état des relais
relay_states = {i: False for i in range(8)}

#def toggle_relay(num):
#    if num in relays:
#        relay_states[num] = not relay_states[num]
#        relays[num].setState(relay_states[num])
#        print(f"Relais {num} {'ON' if relay_states[num] else 'OFF'}")

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

relay_states = {i: False for i in range(8)}

@app.route('/toggle_relay', methods=['POST'])
def toggle_relay():
    data = request.json
    print(request.json)
    print(data)
    relay_id = int(data.get("relay"))
    state = bool(data.get("state"))

    if relay_id in relays:
        relays[relay_id].setState(state)
        relay_states[relay_id] = state
        return jsonify({"status": "success", "relay": relay_id, "state": state})
    
    return jsonify({"status": "error", "message": "Invalid relay"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Désactive le mode debug
