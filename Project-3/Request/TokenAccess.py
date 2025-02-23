import requests

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
    print('infos RTE token = ', infos_rte_token)
else:
    print('Erreur, status code =', response.status_code)
    print('Réponse:', response.text)