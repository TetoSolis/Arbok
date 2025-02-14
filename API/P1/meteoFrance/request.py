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
