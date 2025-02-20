from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import requests
import time
from datetime import datetime
from Phidget22.Devices.DigitalOutput import DigitalOutput

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ECO_FILE = "ecowatt.json"
MODE_FILE = "mode.json"
TOKEN_URL = "https://digital.iservices.rte-france.com/token/oauth"
ECOWATT_URL = "https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals"
AUTH_HEADER = {
    'Authorization': 'Basic OTRlMDkyZjctMjYyYS00NTIwLWFmYTctNDcwNGJlYjAwNjEyOjVmNjYyMTY1LWQ2MDctNGI3Ny1hNjYzLTc0Y2U0NzRlMDc1ZA==',
    'Content-Type': 'application/x-www-form-urlencoded',
}

serial_number = 369498
relays = {}
relay_states = {i: False for i in range(8)}

for i in range(8):
    relay = DigitalOutput()
    relay.setDeviceSerialNumber(serial_number)
    relay.setChannel(i)
    try:
        relay.openWaitForAttachment(5000)
        relay.setState(False)
        relays[i] = relay
    except Exception as e:
        print(f"Erreur d'attachement pour le relais {i}: {e}")

##################################################

def get_oauth_token():
    response = requests.post(TOKEN_URL, headers=AUTH_HEADER)
    if response.status_code == 200:
        return response.json().get("access_token")
    raise HTTPException(status_code=500, detail="Échec de récupération du token OAuth")

##################################################

def fetch_ecowatt_data():
    token = get_oauth_token()
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(ECOWATT_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        with open(ECO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return data
    raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des données Ecowatt")

##################################################

@app.get("/ecowatt")
def get_ecowatt_data():
    if os.path.exists(ECO_FILE):
        with open(ECO_FILE, "r", encoding="utf-8") as f:
            return {"data": json.load(f)}
    return fetch_ecowatt_data()

##################################################

@app.post("/refresh")
def refresh_ecowatt():
    return fetch_ecowatt_data()

##################################################

# Charger le mode actuel
def load_mode():
    try:
        with open(MODE_FILE, "r") as f:
            return json.load(f).get("mode", "auto")
    except FileNotFoundError:
        return "auto"

# Sauvegarder le mode
def save_mode(mode):
    with open(MODE_FILE, "w") as f:
        json.dump({"mode": mode}, f)

@app.post("/mode")
async def set_mode(data: dict):
    mode = data.get("mode")
    if mode not in ["auto", "manual"]:
        raise HTTPException(status_code=400, detail="Mode invalide")

    save_mode(mode)
    return {"mode": mode}

@app.get("/mode")
async def get_mode():
    return {"mode": load_mode()}

##################################################

@app.post("/phidget")
def control_relay(data: dict):
    relay_id = int(data.get("relay"))
    state = bool(data.get("state"))
    if relay_id in relays and relays[relay_id].getAttached():
        relays[relay_id].setState(state)
        relay_states[relay_id] = state
        return {"status": "success", "relay": relay_id, "state": state}
    return {"status": "error", "message": "Relais invalide ou non attaché"}

##################################################

@app.get("/get_relays_state")
def get_relays_state():
    global relay_states  # On modifie le dictionnaire global des relais

    try:
        # Charger les données du fichier EcoWatt
        with open(ECO_FILE, "r") as f:
            data = json.load(f)

        # Récupérer la date du jour au format YYYY-MM-DD
        today = datetime.now().strftime("%Y-%m-%d")

        # Trouver les signaux correspondant à la date du jour
        signal = next((s for s in data.get("signals", []) if s.get("jour", "").startswith(today)), None)

        if not signal:
            print(f"Aucun signal trouvé pour la date {today}")
            return relay_states  # Pas de changement

        # Récupérer l'heure actuelle en tant qu'entier (0-23)
        current_hour = datetime.now().hour

        # Trouver la hvalue correspondant à l'heure actuelle
        value = next((v for v in signal.get("values", []) if v.get("pas") == current_hour), None)

        if value is None:
            print(f"Aucune donnée 'hvalue' trouvée pour {current_hour}h.")
            return relay_states  # Pas de changement

        # Déterminer l'état du relais 1 en fonction de hvalue
        new_state = bool(value.get("hvalue", 0))  # 1 = allumé, 0 = éteint

        # Si l'état change, on met à jour le relais 1
        if relay_states[1] != new_state:
            relay_states[1] = new_state
            if 1 in relays and relays[1].getAttached():
                relays[1].setState(new_state)
                print(f"🔄 Relais 1 mis à {'ON' if new_state else 'OFF'} à {current_hour}h.")
            else:
                print("⚠️ Relais 1 non attaché ou inaccessible.")

    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture du fichier EcoWatt : {e}")

    return relay_states  # Retourne l'état mis à jour des relais

##################################################

@app.post("/update_hvalue")
def update_hvalue(data: dict):
    signal = data.get("signal")
    pas = data.get("pas")
    hvalue = data.get("hvalue")
    if not os.path.exists(ECO_FILE):
        raise HTTPException(status_code=404, detail="Fichier Ecowatt introuvable")

    with open(ECO_FILE, "r") as f:
        data = json.load(f)
        
    # Parcours les signaux et met à jour le hvalue
    for signal_data in data.get("signals"):
        if signal_data.get("jour") == signal:
            print("Jour : ", signal_data.get("jour"))
            for value in signal_data.get("values"):
                if str(value.get("pas")) == pas:
                    print("pas : ", value.get("pas"))
                    value["hvalue"] = hvalue  # Met à jour le hvalue

    # Sauvegarder les modifications dans le fichier
    try:
        with open(ECO_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
       print(f"Erreur lors de l'écriture du fichier : {e}")
       
    get_relays_state()
    print("message : hvalue mis à jour", "signal : ", signal, "pas : ", pas, "hvalue : ", hvalue)
    return {"message": "hvalue mis à jour", "signal": signal, "pas": pas, "hvalue": hvalue}
