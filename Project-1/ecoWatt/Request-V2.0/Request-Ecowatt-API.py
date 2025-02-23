import requests
import json
import os
import time

# 🔹 1. Récupérer le token OAuth
def get_oauth_token():
    url = "https://digital.iservices.rte-france.com/token/oauth"
    headers = {
        'Authorization': 'Basic OTRlMDkyZjctMjYyYS00NTIwLWFmYTctNDcwNGJlYjAwNjEyOjVmNjYyMTY1LWQ2MDctNGI3Ny1hNjYzLTc0Y2U0NzRlMDc1ZA==',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        print("✅ Token récupéré :", token_data['access_token'])
        return token_data['access_token']
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")
        return None

# 🔹 2. Récupérer les données Ecowatt
def fetch_ecowatt_data(token, file_path):
    url = "https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    max_retries = 5
    retry_delay = 10  # secondes
    
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                print(f"✅ Données Ecowatt sauvegardées dans {file_path}")
                return data
            except json.JSONDecodeError:
                print("❌ Erreur: Réponse API non valide")
                return None
        
        elif response.status_code == 429:
            print(f"⚠️ Trop de requêtes, attente {retry_delay} secondes...")
            time.sleep(retry_delay)
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return None

    print("❌ Échec après plusieurs tentatives")
    return None

# 🔹 3. Lire et analyser les données Ecowatt
class Node:
    def __init__(self, jour, pas):
        self.jour = jour
        self.pas = pas
        self.next = None

def add_to_linked_list(head, jour, pas):
    new_node = Node(jour, pas)
    if not head:
        return new_node
    last = head
    while last.next:
        last = last.next
    last.next = new_node
    return head

def analyze_ecowatt_data(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} introuvable")
        return
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    head = None
    for signal in data.get('signals', []):
        jour = signal['jour']
        for entry in signal.get('values', []):
            if entry.get('hvalue') == 0:
                head = add_to_linked_list(head, jour, entry['pas'])

    current = head
    while current:
        print(f"📅 Jour: {current.jour}, ⏰ Heure: {current.pas}h")
        current = current.next

# 🔹 Exécution principale
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "ecowatt.json")
    
    token = get_oauth_token()
    if token:
        ecowatt_data = fetch_ecowatt_data(token, file_path)
        if ecowatt_data:
            analyze_ecowatt_data(file_path)
