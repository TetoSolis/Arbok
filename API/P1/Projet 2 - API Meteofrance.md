# Rapport sur l'Intégration de l'API Météo-France avec OAuth2

## 1. Introduction

L'objectif de ce rapport est de décrire l'intégration de l'API Météo-France en utilisant le protocole d'authentification OAuth2. Cette intégration permet d'accéder aux données météorologiques fournies par Météo-France de manière sécurisée.

## 2. Présentation de l'API Météo-France

L'API Météo-France propose des prévisions météorologiques et des données d'observation en temps réel. L'accès à ces données est protégé par le protocole OAuth2, nécessitant l'obtention d'un jeton d'authentification pour effectuer des requêtes.

## 3. Authentification OAuth2

### 3.1. Obtention du jeton d'accès

Pour interagir avec l'API, il est nécessaire d'obtenir un jeton d'accès en envoyant une requête HTTP POST au serveur d'authentification de Météo-France.

#### Exemple de code en Python :

```python
import requests
import json
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

```

### 3.2. Explication du processus

1. Une requête HTTP POST est envoyée à l'URL d'authentification `https://portail-api.meteofrance.fr/token`.
2. Les crédentials sont envoyés dans les en-têtes sous forme d'une clé `Authorization` encodée en Base64.
3. En cas de succès, un jeton d'accès est retourné et peut être utilisé pour interroger l'API.
4. En cas d'erreur, un message est affiché avec la réponse du serveur.

## 4. Utilisation du jeton pour les requêtes API

Une fois le jeton d'accès obtenu, il doit être inclus dans l'en-tête des requêtes HTTP envoyées à l'API.

### Exemple d'utilisation du jeton pour une requête API dans notre cas :

```python
import requests
import json
import time
import os
import csv
import math

# Déterminer le répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, "meteoFrance.json")

# Fonction pour calculer la distance entre deux points (latitude, longitude) en km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Charger les données JSON
def load_meteo_data():
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

# Trouver la station la plus proche
def find_nearest_station(lat, lon):
    stations = load_meteo_data()
    nearest_station = min(stations, key=lambda station: haversine(lat, lon, station["latitude"], station["longitude"]))
    return nearest_station

# Coordonnées à rechercher
latitude = 47.49520
longitude = 6.802791
nearest = find_nearest_station(latitude, longitude)
print(f"Station la plus proche : {nearest}")

# URL pour obtenir le token
url_token = "https://portail-api.meteofrance.fr/token"

data_token = {'grant_type': 'client_credentials'}
headers_token = {
    'Authorization': 'Basic UGNaSkd4SU9fN3NQSHRNcHJjTENmWnM4M0dBYTp3R25PV1BmM1JkTHlNM2tyWGZQOTdGdFRjajBh',
    'Content-Type': 'application/x-www-form-urlencoded'
}

response_token = requests.post(url_token, data=data_token, headers=headers_token)
status_code = response_token.status_code
print('status code =', status_code)

if status_code == 200:
    infos_meteo_token = response_token.json()
    token_meteo = infos_meteo_token['access_token']
    print('Token Météo France =', token_meteo)
else:
    print(f"Erreur lors de la récupération du token : {response_token.text}")
    exit()

token = infos_meteo_token['access_token']
url = "https://public-api.meteofrance.fr/public/DPObs/v1/liste-stations"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
}

max_retries = 1
retry_delay = 10
for attempt in range(max_retries):
    response = requests.get(url, headers=headers)
    print('Status code =', response.status_code)
    if response.status_code == 200:
        try:
            csv_data = response.text.splitlines()
            csv_reader = csv.reader(csv_data, delimiter=';')
            
            json_data = []
            next(csv_reader, None)  # Ignorer la première ligne (en-têtes)
            
            for row in csv_reader:
                station = {
                    "id": row[0],
                    "wmo": row[1] if row[1] else None,
                    "name": row[2],
                    "latitude": float(row[3]),
                    "longitude": float(row[4]),
                    "altitude": int(row[5]),
                    "start_date": row[6],
                    "type": row[7]
                }
                json_data.append(station)
            
            # Sauvegarde dans un fichier JSON
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, indent=4, ensure_ascii=False)
            print(f"Données enregistrées dans {json_file_path}")
            break
        except Exception as e:
            print("Erreur lors du traitement du CSV:", e)
            break
    elif response.status_code == 429:
        print(f"Erreur 429: Trop de requêtes. Tentative {attempt + 1}/{max_retries}. Réessai dans {retry_delay} sec...")
        time.sleep(retry_delay)
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        break

```

## 5. Conclusion

L'intégration de l'API Météo-France avec OAuth2 permet d'accéder de manière sécurisée aux données météorologiques. Ce processus assure une protection des accès et permet une gestion efficace des requêtes. Les prochaines étapes pourraient inclure l'automatisation de la récupération des données et leur intégration dans un système de prévision ou de monitoring climatique.

