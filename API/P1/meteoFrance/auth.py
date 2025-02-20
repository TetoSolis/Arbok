import requests
import time

# Date fixe : 13 février 2025 à 15h00
date_formatted = "2025-02-12T15:00:00Z"

# URL pour obtenir le token
url_token = "https://portail-api.meteofrance.fr/token"

# Données pour la requête POST
data_token = {
    'grant_type': 'client_credentials',
}

# En-têtes pour l'authentification
headers_token = {
    'Authorization': 'Basic UGNaSkd4SU9fN3NQSHRNcHJjTENmWnM4M0dBYTp3R25PV1BmM1JkTHlNM2tyWGZQOTdGdFRjajBh',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Requête pour obtenir le token
response_token = requests.post(url_token, data=data_token, headers=headers_token)

# Vérification du code de statut et extraction du token
status_code = response_token.status_code
print('status code = ', status_code)

if status_code == 200:
    infos_meteo_token = response_token.json()
    print('Infos Météo France token = ', infos_meteo_token)
    token_meteo = infos_meteo_token['access_token']
    print('Token Météo France = ', token_meteo)
else:
    print(f"Erreur lors de la récupération du token : {response_token.text}")
    exit()

# URL de l'API Ecowatt avec la date fixe du 13 février 2025 à 15h00
url = f"https://public-api.meteofrance.fr/public/DPObs/v1/station/horaire?id_station=90035001&date={date_formatted}&format=json"

# Headers corrigés
headers = {
    "Authorization": f"Bearer {infos_meteo_token['access_token']}",
    "Accept": "application/json",  # Corrige le Content-Type pour demander du JSON
}

# Tentative avec gestion du 429 Too Many Requests
max_retries = 1
retry_delay = 10  # Attendre 10 secondes en cas de 429
for attempt in range(max_retries):
    response = requests.get(url, headers=headers)
    print('Status code =', response.status_code)
    if response.status_code == 200:
        try:
            infos_rte_data_ecowatt_json = response.json()
            print("Données reçues :", infos_rte_data_ecowatt_json)
        
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