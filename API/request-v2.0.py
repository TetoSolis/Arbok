import requests
import time

# URL de Keycloak
url = "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token"

# Informations d'authentification
data = {
    'grant_type': 'client_credentials',   # Type d'authentification
    'client_id': 'abra',          # Client ID défini dans Keycloak
    'client_secret': 'lwGDExe8qiiKGDfM3FFA7hTmfA7W7qUU'  # Secret Keycloak récupéré dans Clients > Credentials
}

# En-têtes HTTP
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Envoi de la requête
response = requests.post(url, data=data, headers=headers)

# Vérification du statut
if response.status_code == 200:
    infos_rte_token = response.json()
    #print('infos RTE token = ', infos_rte_token)
    print('Status code =', response.status_code)
else:
    print('Erreur, status code =', response.status_code)
    print('Réponse:', response.text)

# Fichier où enregistrer les données

# Token d'accès (remplace par un token valide si nécessaire)
token = infos_rte_token['access_token']
#token = ''
# URL de l'API Ecowatt
url = "http://localhost:5000/api"

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
    
