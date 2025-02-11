import requests
import json
import time

# Fichier où enregistrer les données
file = "ecowatt.json"

# Token d'accès (remplace par un token valide si nécessaire)
token = "4WtoA7oY30PPlHc4Ihcl7PYlMlDvIrx66WPcbUiATomYydBl666tbT"

# URL de l'API Ecowatt
url = "https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals"

# Headers corrigés
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",  # Corrige le Content-Type pour demander du JSON
}

# Tentative avec gestion du 429 Too Many Requests
max_retries = 5
retry_delay = 10  # Attendre 10 secondes en cas de 429
for attempt in range(max_retries):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            infos_rte_data_ecowatt_json = response.json()
            print("Données reçues :", infos_rte_data_ecowatt_json)
            
            # Sauvegarde en fichier JSON
            with open(file, "w") as f:
                json.dump(infos_rte_data_ecowatt_json, f, indent=4)
            print(f"Données sauvegardées dans {file}")
            break
        
        except requests.exceptions.JSONDecodeError:
            print("Erreur: La réponse de l'API n'est pas un JSON valide.")
            print("Réponse brute:", response.text)
            break  # Sortir de la boucle car ce n'est pas un problème de rate limit

    elif response.status_code == 429:
        print(f"Erreur 429: Trop de requêtes. Tentative {attempt + 1}/{max_retries}. Réessai dans {retry_delay} sec...")
        time.sleep(retry_delay)
    
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        break
