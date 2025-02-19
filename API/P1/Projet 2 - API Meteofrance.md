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

# URL pour obtenir le token
url_token = "https://portail-api.meteofrance.fr/token"

# Données pour la requête POST
data_token = {'grant_type': 'client_credentials'}
headers_token = {
    'Authorization': 'Basic UGNaSkd4SU9fN3NQSHRNcHJjTENmWnM4M0dBYTp3R25PV1BmM1JkTHlNM2tyWGZQOTdGdFRjajBh',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Envoi de la requête pour obtenir le token
response_token = requests.post(url_token, data=data_token, headers=headers_token)

if response_token.status_code == 200:
    token_meteo = response_token.json().get('access_token')
    print('Token Météo-France =', token_meteo)
else:
    print(f"Erreur lors de la récupération du token : {response_token.text}")
```

### 3.2. Explication du processus

1. Une requête HTTP POST est envoyée à l'URL d'authentification `https://portail-api.meteofrance.fr/token`.
2. Les crédentials sont envoyés dans les en-têtes sous forme d'une clé `Authorization` encodée en Base64.
3. En cas de succès, un jeton d'accès est retourné et peut être utilisé pour interroger l'API.
4. En cas d'erreur, un message est affiché avec la réponse du serveur.

## 4. Utilisation du jeton pour les requêtes API

Une fois le jeton d'accès obtenu, il doit être inclus dans l'en-tête des requêtes HTTP envoyées à l'API.

### Exemple d'utilisation du jeton pour une requête API :

```python
headers = {
    "Authorization": f"Bearer {token_meteo}",
    "Accept": "application/json",
}
url_api = "https://public-api.meteofrance.fr/public/DPObs/v1/liste-stations"

response = requests.get(url_api, headers=headers)
print(response.json())
```

## 5. Conclusion

L'intégration de l'API Météo-France avec OAuth2 permet d'accéder de manière sécurisée aux données météorologiques. Ce processus assure une protection des accès et permet une gestion efficace des requêtes. Les prochaines étapes pourraient inclure l'automatisation de la récupération des données et leur intégration dans un système de prévision ou de monitoring climatique.

