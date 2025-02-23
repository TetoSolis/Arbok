***
## **Sommaire du Projet : Sécurisation d’une API avec OAuth2 sur Raspberry Pi et ESP32**

### 1. **Introduction**

- **1.1 Objectifs du projet**
    - Créer une API sur un Raspberry Pi et un ESP32 pour la gestion de capteurs et la communication avec des applications externes.
    - Implémenter la sécurisation de cette API en utilisant le protocole OAuth2, afin de garantir l'accès uniquement aux utilisateurs autorisés.
    - Utiliser Keycloak pour gérer l'authentification et l'autorisation des utilisateurs.
- **1.2 Présentation des composants utilisés**
    - **Raspberry Pi** : Serveur pour l'API Flask.
    - **ESP32** : Dispositif embarqué pour interagir avec des capteurs et exposer des endpoints RESTful.
    - **Keycloak** : Serveur d'authentification pour gérer les tokens OAuth2.
    - **Capteur DS18B20** : Pour récupérer des données de température.

---

### 2. **Architecture du Projet**
- **2.1 Description de l’architecture générale**
    - L'API est exposée à partir d'un Raspberry Pi avec Flask, sécurisée par OAuth2 pour les accès.
    - L'ESP32 se connecte au serveur via Wi-Fi et expose un endpoint REST pour récupérer des données de température en utilisant un capteur DS18B20.
    - Keycloak gère l'authentification des utilisateurs via des tokens OAuth2.
- **2.2 Schéma d’architecture**
    - Raspberry Pi <-> Keycloak (authentification) <-> ESP32 <-> Capteur DS18B20
---
### 3. **Mise en place de l’API avec Flask sur Raspberry Pi**
- **3.1 Installation des dépendances nécessaires**
    - Installation de Flask, Requests, et autres librairies pour l’API.
- **3.2 Création des endpoints de l’API**
    - Endpoint `/counter` pour la gestion d’un compteur, sécurisé par OAuth2.
- **3.3 Implémentation de la gestion des tokens OAuth2**
    - Utilisation de Keycloak pour récupérer et valider les tokens OAuth2.
---
### 4. **Sécurisation de l’API avec OAuth2**
- **4.1 Présentation du protocole OAuth2**
    - Explication du protocole OAuth2 et de son rôle dans la sécurisation des APIs.
    - Utilisation des tokens d'accès pour autoriser les requêtes.
- **4.2 Configuration de Keycloak**
    - Création d'un realm et d'un client dans Keycloak pour générer des tokens d’accès.
    - Paramétrage des credentials pour l’authentification.
- **4.3 Implémentation de la vérification des tokens**
    - Validation des tokens via une introspection avec Keycloak pour s’assurer de leur validité avant d'autoriser l'accès à l’API.
---
### 5. **Implémentation sur l’ESP32**
- **5.1 Configuration Wi-Fi sur ESP32**
    - Connexion à un réseau Wi-Fi avec une IP statique.
- **5.2 Lecture des données de température avec le capteur DS18B20**
    - Mise en place du capteur DS18B20 pour récupérer les données de température.
- **5.3 Création d’un serveur Web pour exposer les données**
    - Implémentation d’un serveur HTTP avec WebServer pour gérer les requêtes et retourner les données sous forme de JSON.
- **5.4 Sécurisation de l’accès à l’API ESP32 avec OAuth2**
    - Vérification des tokens envoyés avec chaque requête pour s’assurer que l’utilisateur est autorisé à accéder aux données de température.
---
### 8. **Conclusion**
- **8.1 Bilan des objectifs atteints**
    - Création d’une API sécurisée et fonctionnelle pour la gestion des capteurs, avec un contrôle d'accès via OAuth2.
- **8.2 Impact du projet**
    - Sécurisation des échanges de données dans un environnement IoT, garantissant ainsi la confidentialité et l'intégrité des informations.
- **8.3 Perspectives d’évolution**
    - Ajout d’autres capteurs IoT, amélioration de l’interface utilisateur, et gestion avancée des tokens (expiration, renouvellement).

***

### 1. **Introduction**

#### **1.1 Objectifs du projet**

L'objectif principal de ce projet est de créer une infrastructure sécurisée pour la gestion de capteurs IoT en utilisant une API sur un Raspberry Pi et un ESP32. Cette API permet aux applications externes de communiquer avec des capteurs, tout en garantissant que seules les personnes autorisées puissent accéder aux données sensibles grâce à l'utilisation du protocole OAuth2. L'authentification et l'autorisation des utilisateurs sont gérées par Keycloak, un serveur d'identité open-source qui fournit des mécanismes d'authentification robustes.

Les objectifs spécifiques incluent :

1. **Création d'une API RESTful** sur le Raspberry Pi et l'ESP32 pour l'interaction avec des capteurs IoT (comme le DS18B20 pour la température).
2. **Implémentation de la sécurité OAuth2** pour assurer que seules les requêtes autorisées puissent accéder aux informations des capteurs, en utilisant des tokens d'accès.
3. **Utilisation de Keycloak** comme serveur d'authentification et d'autorisation pour gérer la délivrance de tokens et la vérification de leur validité avant de permettre l'accès aux ressources exposées par l'API.

Cette architecture permet de centraliser la gestion des capteurs, de sécuriser les échanges de données et de simplifier l'intégration avec d'autres services ou applications, tout en offrant une couche de sécurité nécessaire pour les environnements sensibles.

#### **1.2 Présentation des composants utilisés**

- **Raspberry Pi** : Le Raspberry Pi sert de serveur principal pour l'API. Il exécute un environnement Flask qui gère les requêtes HTTP des utilisateurs, et expose des endpoints permettant d'interagir avec les capteurs IoT. Dans ce projet, Flask permet de construire des APIs légères et simples pour récupérer des données du capteur et gérer la sécurisation via OAuth2. Le Raspberry Pi communique avec l'ESP32 pour centraliser les données recueillies par les capteurs IoT.
    
- **ESP32** : L'ESP32 est un microcontrôleur puissant et économique avec des capacités Wi-Fi et Bluetooth. Il est utilisé pour collecter des données de capteurs, comme les mesures de température fournies par le capteur DS18B20, et pour exposer une API RESTful qui permet d'accéder à ces données. L'ESP32 se connecte au Raspberry Pi via le réseau Wi-Fi pour envoyer ces données, et utilise également OAuth2 pour sécuriser l'accès à ses endpoints, en validant les tokens d'accès fournis par les utilisateurs.
    
- **Keycloak** : Keycloak est une solution open-source de gestion d'identités et d'accès, qui fournit des services d'authentification et d'autorisation. Dans ce projet, Keycloak est utilisé pour gérer la délivrance de tokens OAuth2 via l'authentification client. Lorsqu'un client (comme l'ESP32 ou une application externe) envoie une requête d'accès à l'API, Keycloak est utilisé pour émettre un token d'accès valide, qui sera ensuite vérifié avant d'accorder l'accès aux données. Keycloak permet de garantir que seules les requêtes authentifiées et autorisées puissent accéder aux ressources protégées.
    
- **Capteur DS18B20** : Le DS18B20 est un capteur de température numérique qui communique avec les microcontrôleurs via le bus OneWire. Ce capteur permet de mesurer la température ambiante avec une grande précision. Il est connecté à l'ESP32, et ses données sont exposées via une API RESTful sécurisée par OAuth2. Ces données peuvent ensuite être utilisées par d'autres systèmes ou applications qui ont les autorisations nécessaires pour y accéder.
    

### 2. **Architecture du système**

#### **2.1 Schéma de communication**

Dans ce projet, l'architecture repose sur une communication entre plusieurs composants :

1. **Raspberry Pi** : Sert de serveur principal avec l'API Flask qui gère la logique des requêtes, l'authentification, et la gestion des utilisateurs via OAuth2.
2. **ESP32** : Récupère les données des capteurs (telles que la température) et les expose via une API RESTful. Il valide également les tokens OAuth2 reçus dans les en-têtes des requêtes pour s'assurer que l'accès est autorisé.
3. **Keycloak** : Fournit un mécanisme centralisé d'authentification et d'autorisation via OAuth2, permettant à l'ESP32 et à d'autres clients d'obtenir des tokens d'accès.
4. **Applications externes** : Ces applications envoient des requêtes à l'ESP32 via l'API RESTful, en utilisant un token OAuth2 valide pour accéder aux ressources protégées.

#### **2.2 Sécurisation via OAuth2**

L'un des aspects les plus importants du projet est la sécurisation des accès via OAuth2, un protocole d'autorisation largement utilisé. Le processus fonctionne comme suit :

1. **Obtention d'un token d'accès** : Les clients (comme l'ESP32 ou une application externe) s'authentifient auprès de Keycloak en utilisant des informations d'identification (client_id et client_secret). Keycloak délivre un token d'accès OAuth2.
2. **Vérification du token** : Lorsqu'une requête est envoyée à l'API, le serveur Flask ou l'ESP32 extrait le token de l'en-tête "Authorization" de la requête. Il contacte Keycloak pour vérifier si le token est valide. Si le token est valide, la requête est autorisée à accéder aux données protégées. Sinon, une réponse d'erreur est renvoyée (401 ou 403).
3. **Accès aux données** : Si le token est valide, l'ESP32 renvoie les données des capteurs, telles que la température du DS18B20, sous forme de réponse JSON.
#### **2.3 Gestion des capteurs**

Les capteurs IoT, comme le DS18B20, sont gérés directement par l'ESP32. Les données collectées sont ensuite envoyées à l'API exposée par l'ESP32. L'ESP32 fournit des endpoints pour interroger les capteurs et récupérer les valeurs de température. Ces endpoints sont sécurisés et nécessitent une authentification via OAuth2.

### 3. **Mise en place de l’API avec Flask sur Raspberry Pi**

#### **3.1 Installation des dépendances nécessaires**

Avant de commencer à développer l'API, vous devez installer les dépendances nécessaires sur votre Raspberry Pi. Nous allons utiliser Flask pour le framework web et Requests pour interagir avec Keycloak pour l'authentification OAuth2.

Voici les étapes pour installer les dépendances :

1. **Mettre à jour votre système** : Ouvrez un terminal sur votre Raspberry Pi et mettez à jour vos paquets :
```bash
sudo apt update && sudo apt upgrade
```
2. **Installer Python3 et pip** (si non déjà installé) :
```bash
sudo apt install python3 python3-pip
```
1. **Installer Flask et Requests** :
Flask est le framework web léger que nous utiliserons pour créer notre API, et Requests est une bibliothèque pour envoyer des requêtes HTTP et gérer les tokens OAuth2.
Installez-les via pip :
```bash
pip3 install Flask requests
```

#### **3.2 Création des endpoints de l’API**

Une fois les dépendances installées, nous pouvons créer un simple serveur Flask et définir les endpoints de l'API.

Voici un exemple d’implémentation avec un endpoint `/counter`, qui gère un compteur et est protégé par OAuth2 :
```python
import os
import requests
from flask import Flask, jsonify, request
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Configuration Keycloak
KEYCLOAK_URL = "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token"
CLIENT_ID = "abra"
CLIENT_SECRET = "qc3c05GiFknf1io0vAOAsOETpgGdOkSD"
SCOPE = "psyko"

counter = 0

def get_access_token():
    """
    Cette fonction récupère un token d'accès OAuth2 en envoyant une requête POST à Keycloak.
    """
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPE
    }
    
    response = requests.post(KEYCLOAK_URL, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Erreur lors de l'obtention du token : {response.text} (Code: {response.status_code})")

def verify_token(token):
    """
    Cette fonction valide un token d'accès en interrogeant Keycloak.
    """
    introspect_url = f"http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token/introspect"
    response = requests.post(introspect_url, data={
        'token': token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    
    if response.status_code == 200:
        return response.json().get("active", False)
    else:
        return False

@app.route('/counter', methods=['GET'])
def api():
    """
    Endpoint pour incrémenter et renvoyer la valeur du compteur.
    Sécurisé avec OAuth2.
    """
    global counter

    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    token = auth_header.split(" ")[1] if len(auth_header.split()) == 2 else None
    
    if not token:
        return jsonify({"error": "Token missing in Authorization header"}), 401
    
    try:
        if not verify_token(token):
            return jsonify({"error": "Invalid token"}), 401

        counter += 1
        return jsonify({"result": counter})

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
```
Dans cet exemple, l'endpoint `/counter` :

- **Incrémente un compteur** chaque fois qu'il est appelé.
- **Est sécurisé par OAuth2** en exigeant un token d'accès valide. Si le token est absent ou invalide, la réponse sera une erreur 401.
- **Utilise Keycloak pour la validation du token**.

#### **Explication du code :**

- **get_access_token** : Cette fonction obtient un token OAuth2 en faisant une requête à Keycloak. Elle utilise les informations d'identification du client (client_id et client_secret) pour obtenir un token d'accès via la méthode `client_credentials`.
    
- **verify_token** : Cette fonction vérifie un token d'accès en envoyant une requête à l'endpoint `introspect` de Keycloak. Ce service permet de valider si le token est toujours actif et valide.
    
- **/counter** : Ce endpoint gère un compteur simple. Lorsqu'il est appelé, il vérifie que le token d'accès dans l'en-tête `Authorization` est valide avant d'incrémenter et de renvoyer la valeur du compteur. Si le token est invalide ou manquant, il renverra une erreur 401.
    

#### **3.3 Implémentation de la gestion des tokens OAuth2**

L'authentification OAuth2 dans ce cas repose sur l'utilisation de **Keycloak** pour la gestion des tokens. Le processus fonctionne comme suit :

1. **Obtention du token d'accès** :
    
    - L'API Flask demande un token d'accès à Keycloak à l'aide des informations d'identification du client (client_id et client_secret).
    - Si la demande est réussie, Keycloak renvoie un **token d'accès** (Access Token).
2. **Validation du token** :
    
    - Lorsqu'une requête est envoyée à l'API Flask, le serveur vérifie si l'en-tête `Authorization` contient un token valide.
    - Si un token est présent, la fonction `verify_token` contacte Keycloak pour vérifier la validité du token via l'endpoint `introspect`.
    - Si le token est valide, l'API exécute la logique demandée (par exemple, incrémenter le compteur).
    - Si le token est invalide, l'API renvoie une réponse d'erreur 401.
3. **Accès sécurisé aux ressources** :
    
    - Si le token est valide, l'utilisateur peut accéder à l'API et obtenir les données ou interagir avec les ressources exposées. Si le token est invalide, l'accès est refusé.

### Test de l’API

Pour tester l'API, vous pouvez utiliser **Postman** ou **cURL** pour envoyer des requêtes HTTP GET avec un token valide dans l'en-tête `Authorization` :

1. **Obtenir un token** via l'endpoint `token` de Keycloak.
2. **Envoyer une requête à l'API** avec le token dans l'en-tête `Authorization`.
```bash
curl -X GET http://<IP_RASPBERRY_PI>:5000/counter -H "Authorization: Bearer <VOTRE_TOKEN>"
```
Cela renverra la valeur du compteur si le token est valide, ou une erreur 401 si le token est invalide.

### 4. **Sécurisation de l’API avec OAuth2**

#### **4.1 Présentation du protocole OAuth2**

OAuth2 (Open Authorization 2) est un protocole standard pour l'autorisation d'accès à des ressources protégées, tout en permettant de partager des données et services entre applications, sans avoir à fournir directement les informations sensibles telles que les mots de passe.

Il fonctionne en permettant à une application (client) d'obtenir un accès limité à des ressources détenues par un utilisateur, via un **token d'accès** généré par un fournisseur d'identité (par exemple, Keycloak).

Voici les principaux composants du protocole OAuth2 :

- **Resource Owner (Propriétaire de la ressource)** : Utilisateur qui accorde l'accès à ses ressources (par exemple, un utilisateur).
- **Client** : L'application qui demande un accès aux ressources (par exemple, l'API Flask).
- **Authorization Server** : Serveur qui délivre les tokens d'accès après avoir authentifié l'utilisateur (par exemple, Keycloak).
- **Resource Server** : Serveur qui héberge les ressources protégées (par exemple, l'API Flask).

Le client demande des tokens d'accès au serveur d'autorisation, puis utilise ces tokens pour accéder aux ressources protégées sur le serveur de ressources. Ce processus permet de garantir que seules les entités autorisées peuvent accéder à ces ressources.

**Types de tokens :**

- **Access Token** : C'est le principal token utilisé pour l'accès à une ressource protégée. Il est généralement éphémère et expirera après un certain temps.
- **Refresh Token** : Permet de récupérer un nouveau token d'accès sans que l'utilisateur ait à se reconnecter.

**Avantages de OAuth2** :

- **Sécurisation de l’accès** : Permet de sécuriser l’accès aux ressources en limitant l’exposition des mots de passe.
- **Contrôle granulaire** : Il est possible de définir les permissions et d’accorder l’accès à des parties spécifiques des données.
- **Token à durée limitée** : Réduit le risque de compromission en ayant des tokens avec une durée de vie limitée.

#### **4.2 Configuration de Keycloak**

Keycloak est une solution d'authentification et de gestion des accès, compatible avec OAuth2, qui vous permet de gérer les utilisateurs, les permissions, et de sécuriser votre API avec des tokens.

Voici les étapes pour configurer Keycloak et générer des tokens d'accès pour votre API :

1. **Installation et configuration de Keycloak** : Si vous n'avez pas encore installé Keycloak, vous pouvez le faire en suivant les instructions sur le site officiel : Keycloak Installation.
    
2. **Création d’un Realm** : Un **realm** dans Keycloak est un espace d'isolation où vous pouvez gérer les utilisateurs, rôles, clients, etc.
    
    - Connectez-vous à l'interface d'administration de Keycloak.
    - Cliquez sur **"Add realm"** et créez un nouveau **realm** (par exemple, `Abo`).
3. **Création d’un Client** : Un **client** dans Keycloak représente une application qui interagit avec Keycloak pour l'authentification.
    
    - Dans le **realm** créé, allez dans **Clients** et cliquez sur **Create**.
    - Entrez un nom pour le client (par exemple, `my-api-client`) et choisissez **OpenID Connect** comme protocole.
    - Définissez l'**Access Type** sur **Confidential** si vous utilisez des identifiants de client secrets (comme dans ce cas).
    - Entrez l'URL de redirection (si nécessaire pour des flux d'autorisation comme `http://localhost:5000/callback`).
4. **Configuration des Credentials du Client** :
    
    - Une fois le client créé, vous trouverez une section **Credentials** où vous trouverez le **Client Secret**.
    - Vous devrez utiliser ces informations dans votre API Flask pour obtenir un token OAuth2.
5. **Création de Rôles et Groupes (facultatif)** : Si vous souhaitez avoir un contrôle plus granulaire sur les accès, vous pouvez créer des rôles dans Keycloak, et les associer à des utilisateurs.
    
6. **Configuration du flow OAuth2 dans Keycloak** :
    
    - Vous pouvez configurer différents flows d'authentification dans Keycloak, par exemple, le flow **Client Credentials** qui permet à une application d’obtenir un token d'accès sans nécessiter l’interaction de l’utilisateur.

#### **4.3 Implémentation de la vérification des tokens**

Une fois Keycloak configuré et que l'application peut obtenir un token d'accès via OAuth2, il est nécessaire de vérifier la validité de ce token avant de lui accorder l'accès à l'API.

Voici comment implémenter la vérification des tokens dans votre API Flask.

1. **Obtenir le token d’accès** : Lorsqu'une requête est envoyée à l'API, le client doit fournir le token d’accès dans l’en-tête `Authorization` sous la forme suivante :

Le client demande des tokens d'accès au serveur d'autorisation, puis utilise ces tokens pour accéder aux ressources protégées sur le serveur de ressources. Ce processus permet de garantir que seules les entités autorisées peuvent accéder à ces ressources.

**Types de tokens :**

- **Access Token** : C'est le principal token utilisé pour l'accès à une ressource protégée. Il est généralement éphémère et expirera après un certain temps.
- **Refresh Token** : Permet de récupérer un nouveau token d'accès sans que l'utilisateur ait à se reconnecter.

**Avantages de OAuth2** :

- **Sécurisation de l’accès** : Permet de sécuriser l’accès aux ressources en limitant l’exposition des mots de passe.
- **Contrôle granulaire** : Il est possible de définir les permissions et d’accorder l’accès à des parties spécifiques des données.
- **Token à durée limitée** : Réduit le risque de compromission en ayant des tokens avec une durée de vie limitée.

#### **4.2 Configuration de Keycloak**

Keycloak est une solution d'authentification et de gestion des accès, compatible avec OAuth2, qui vous permet de gérer les utilisateurs, les permissions, et de sécuriser votre API avec des tokens.

Voici les étapes pour configurer Keycloak et générer des tokens d'accès pour votre API :

1. **Installation et configuration de Keycloak** : Si vous n'avez pas encore installé Keycloak, vous pouvez le faire en suivant les instructions sur le site officiel : Keycloak Installation.
    
2. **Création d’un Realm** : Un **realm** dans Keycloak est un espace d'isolation où vous pouvez gérer les utilisateurs, rôles, clients, etc.
    
    - Connectez-vous à l'interface d'administration de Keycloak.
    - Cliquez sur **"Add realm"** et créez un nouveau **realm** (par exemple, `Abo`).
3. **Création d’un Client** : Un **client** dans Keycloak représente une application qui interagit avec Keycloak pour l'authentification.
    
    - Dans le **realm** créé, allez dans **Clients** et cliquez sur **Create**.
    - Entrez un nom pour le client (par exemple, `my-api-client`) et choisissez **OpenID Connect** comme protocole.
    - Définissez l'**Access Type** sur **Confidential** si vous utilisez des identifiants de client secrets (comme dans ce cas).
    - Entrez l'URL de redirection (si nécessaire pour des flux d'autorisation comme `http://localhost:5000/callback`).
4. **Configuration des Credentials du Client** :
    
    - Une fois le client créé, vous trouverez une section **Credentials** où vous trouverez le **Client Secret**.
    - Vous devrez utiliser ces informations dans votre API Flask pour obtenir un token OAuth2.
5. **Création de Rôles et Groupes (facultatif)** : Si vous souhaitez avoir un contrôle plus granulaire sur les accès, vous pouvez créer des rôles dans Keycloak, et les associer à des utilisateurs.
    
6. **Configuration du flow OAuth2 dans Keycloak** :
    
    - Vous pouvez configurer différents flows d'authentification dans Keycloak, par exemple, le flow **Client Credentials** qui permet à une application d’obtenir un token d'accès sans nécessiter l’interaction de l’utilisateur.

#### **4.3 Implémentation de la vérification des tokens**

Une fois Keycloak configuré et que l'application peut obtenir un token d'accès via OAuth2, il est nécessaire de vérifier la validité de ce token avant de lui accorder l'accès à l'API.

Voici comment implémenter la vérification des tokens dans votre API Flask.

1. **Obtenir le token d’accès** : Lorsqu'une requête est envoyée à l'API, le client doit fournir le token d’accès dans l’en-tête `Authorization` sous la forme suivante :
```
Authorization: Bearer <token>
```

2. **Vérification du token via Keycloak** : Keycloak offre un endpoint d’introspection pour vérifier la validité d’un token d’accès. Cela vous permet de savoir si un token est encore valide, s'il a expiré, ou s'il a été révoqué.

Voici comment vérifier un token dans Flask :
```python
def verify_token(token):
    """
    Cette fonction valide un token d'accès en interrogeant Keycloak.
    """
    introspect_url = "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token/introspect"
    response = requests.post(introspect_url, data={
        'token': token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    
    if response.status_code == 200:
        return response.json().get("active", False)
    else:
        return False
```
- - L'endpoint `token/introspect` est utilisé pour envoyer une requête POST à Keycloak, en lui fournissant le token, le client_id, et le client_secret.
    - Si la réponse de Keycloak indique que le token est **actif**, l'accès est autorisé, sinon il est rejeté.
- **Utilisation de la fonction de validation dans l’API** : Vous utilisez la fonction `verify_token` dans votre endpoint pour vous assurer que chaque requête est accompagnée d’un token valide avant d’exécuter la logique de l’API.
    Exemple dans un endpoint :
```python
@app.route('/counter', methods=['GET'])
def api():
    """
    Endpoint pour incrémenter et renvoyer la valeur du compteur.
    Sécurisé avec OAuth2.
    """
    global counter
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401
    token = auth_header.split(" ")[1] if len(auth_header.split()) == 2 else None
    if not token:
        return jsonify({"error": "Token missing in Authorization header"}), 401
    try:
        if not verify_token(token):
            return jsonify({"error": "Invalid token"}), 401
        counter += 1
        return jsonify({"result": counter})
    except Exception as e:
        return jsonify({"error": str(e)}), 401
```
#### **Résumé des étapes de sécurisation :**

- **Configurer Keycloak** : Créer un **realm** et un **client**, et générer un **client secret** pour l’authentification.
- **Obtenir un token d'accès** : Utiliser OAuth2 pour obtenir un token d’accès via Keycloak.
- **Vérification du token** : Implémenter une validation du token via l’introspection à Keycloak avant d’autoriser l’accès à l’API.
- **Accès sécurisé** : Utiliser ce token pour sécuriser l'accès à vos endpoints et garantir que seules les entités autorisées puissent interagir avec votre API.

### 5. **Implémentation sur l’ESP32**

#### **5.1 Configuration Wi-Fi sur ESP32**

Pour connecter l'ESP32 à un réseau Wi-Fi avec une adresse IP statique, vous devez utiliser la bibliothèque `WiFi.h`. Vous pouvez spécifier les paramètres de votre réseau, tels que le SSID, le mot de passe et l'adresse IP statique, ainsi que le masque de sous-réseau et la passerelle.

Voici un exemple pour configurer l'ESP32 :
```cpp
#include <WiFi.h>

const char* ssid = "NomDuReseau";  // Remplacer par le SSID de votre réseau
const char* password = "MotDePasse";  // Remplacer par le mot de passe de votre réseau

IPAddress ip(192, 168, 1, 184);      // Adresse IP statique
IPAddress gateway(192, 168, 1, 1);  // Passerelle
IPAddress subnet(255, 255, 255, 0); // Masque de sous-réseau

void setup() {
  Serial.begin(115200);
  
  // Connexion au Wi-Fi avec une adresse IP statique
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);

  // Attente de la connexion Wi-Fi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion en cours...");
  }
  
  Serial.println("Connexion Wi-Fi réussie");
  Serial.print("IP de l'ESP32 : ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Code principal
}
```
Ce code configure l'ESP32 pour se connecter à un réseau Wi-Fi avec une adresse IP statique et imprime l'IP sur le moniteur série une fois connecté.

#### **5.2 Lecture des données de température avec le capteur DS18B20**

Le capteur DS18B20 utilise le protocole **OneWire** pour communiquer avec les microcontrôleurs. Pour l'utiliser avec l'ESP32, vous devez installer la bibliothèque **OneWire** et **DallasTemperature**.

Voici un exemple pour lire la température avec un capteur DS18B20 connecté à la broche **D2** (GPIO4) :
```cpp
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 4  // Pin de connexion du DS18B20

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures(); // Demande des données de température

  float temperatureC = sensors.getTempCByIndex(0); // Lecture de la température en Celsius

  Serial.print("Température: ");
  Serial.print(temperatureC);
  Serial.println(" °C");

  delay(2000); // Délai entre les lectures
}
```
Ce code lit la température du capteur DS18B20 et l'affiche toutes les 2 secondes sur le moniteur série.

#### **5.3 Création d’un serveur Web pour exposer les données**

L’ESP32 peut être utilisé pour héberger un serveur HTTP afin d'exposer les données sous forme de JSON. Vous pouvez utiliser la bibliothèque **ESPAsyncWebServer** pour cela.

Voici un exemple pour configurer un serveur HTTP qui expose les données de température :
```cpp
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 4  // Pin de connexion du DS18B20
const char* ssid = "NomDuReseau";
const char* password = "MotDePasse";

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);

  // Connexion au Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion au Wi-Fi...");
  }

  Serial.println("Connexion réussie !");
  Serial.print("IP de l'ESP32 : ");
  Serial.println(WiFi.localIP());

  sensors.begin();

  // Endpoint pour obtenir les données de température
  server.on("/temperature", HTTP_GET, [](AsyncWebServerRequest *request){
    sensors.requestTemperatures(); 
    float temperatureC = sensors.getTempCByIndex(0);

    String jsonResponse = "{\"temperature\": " + String(temperatureC) + "}";
    request->send(200, "application/json", jsonResponse);
  });

  // Démarrage du serveur
  server.begin();
}

void loop() {
  // Le serveur HTTP tourne en arrière-plan, rien à ajouter ici.
}
```
Ce code crée un serveur HTTP sur l'ESP32 qui écoute sur le port 80. Lorsqu'une requête GET est envoyée à `/temperature`, il retourne les données de température sous forme de JSON, par exemple :
```json
{"temperature": 23.45}
```

#### **5.4 Sécurisation de l’accès à l’API ESP32 avec OAuth2**

Pour sécuriser l'accès à l'API sur l'ESP32 avec OAuth2, l'ESP32 doit valider les tokens d'accès envoyés par les clients (comme l'API Flask). Vous devez vérifier que le token est valide avant de retourner les données du capteur.

Voici un exemple de vérification d'un token OAuth2 dans l'ESP32. Vous devrez intégrer une bibliothèque HTTP pour envoyer une requête de validation à Keycloak. Cela peut être fait en utilisant une API d'introspection.

1. **Obtenir le token d'accès** : Le client envoie une requête GET à `/temperature` avec un en-tête `Authorization` contenant le token :
```
Authorization: Bearer <token>
```

2. **Vérification du token via Keycloak** : L'ESP32 devra envoyer une requête POST à l'endpoint d'introspection de Keycloak pour valider le token.
    

Voici un code pour valider le token via Keycloak sur l'ESP32 :
```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* keycloakUrl = "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token/introspect";
const char* clientId = "my-api-client";
const char* clientSecret = "my-client-secret";

bool verifyToken(String token) {
  HTTPClient http;
  http.begin(keycloakUrl);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  String body = "token=" + token + "&client_id=" + clientId + "&client_secret=" + clientSecret;

  int httpCode = http.POST(body);

  if (httpCode == 200) {
    String payload = http.getString();
    if (payload.indexOf("\"active\":true") != -1) {
      return true;
    }
  }
  return false;
}
```
Dans ce code, la fonction `verifyToken` envoie une requête POST à l'endpoint d'introspection de Keycloak pour vérifier si le token est valide. Si le token est valide, la fonction retourne `true`, sinon elle retourne `false`.

3. **Protection de l’endpoint** : Vous pouvez protéger l'endpoint `/temperature` en vérifiant le token avant de retourner les données :
```cpp
server.on("/temperature", HTTP_GET, [](AsyncWebServerRequest *request){
  String token = request->getHeader("Authorization").substring(7); // Récupère le token (retire "Bearer ")

  if (!verifyToken(token)) {
    request->send(401, "application/json", "{\"error\": \"Invalid or expired token\"}");
    return;
  }

  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  String jsonResponse = "{\"temperature\": " + String(temperatureC) + "}";
  request->send(200, "application/json", jsonResponse);
});
```
Dans ce code, l'ESP32 vérifie le token d'accès avant de permettre l'accès aux données du capteur. Si le token est invalide, une réponse `401 Unauthorized` est envoyée.

### 6. **Conclusion**

#### **6.1 Bilan des objectifs atteints**

Le projet a permis de réaliser une API sécurisée et fonctionnelle pour la gestion de capteurs IoT, en particulier avec l'ESP32 et un capteur de température DS18B20. L'API a été protégée par le protocole OAuth2, avec l'utilisation de Keycloak pour l'authentification et la gestion des tokens d'accès. Les principales étapes ont été franchies avec succès :

- Mise en place de l'API Flask sur le Raspberry Pi.
- Création des endpoints nécessaires pour l’interaction avec les capteurs.
- Implémentation de la sécurité avec OAuth2 et validation des tokens via Keycloak.
- Développement du serveur Web sur l'ESP32 pour exposer les données des capteurs avec une interface sécurisée.

L'ensemble des objectifs fixés en début de projet a été atteint, et l'API est désormais prête à interagir avec des applications externes tout en garantissant une sécurité optimale.

#### **6.2 Impact du projet**

Ce projet a un impact significatif dans le domaine de l'Internet des objets (IoT), notamment pour les applications nécessitant des échanges sécurisés de données sensibles entre des dispositifs embarqués et des serveurs. En implémentant OAuth2 pour sécuriser les accès à l'API, le projet permet :

- **Confidentialité des données** : Seules les applications ou utilisateurs autorisés peuvent accéder aux informations provenant des capteurs.
- **Intégrité des échanges** : La vérification des tokens OAuth2 garantit que les données n'ont pas été altérées et que les requêtes proviennent bien de sources de confiance.
- **Évolutivité** : La solution permet l'ajout de nouveaux capteurs ou modules sans compromettre la sécurité de l'ensemble du système.

L'usage de Keycloak comme serveur d'authentification centralisé apporte également une souplesse importante dans la gestion des utilisateurs, avec la possibilité de définir des rôles et des permissions détaillées.

#### **6.3 Perspectives d’évolution**

Le projet peut évoluer de plusieurs manières pour étendre ses fonctionnalités et améliorer sa sécurité et son expérience utilisateur :

1. **Ajout d’autres capteurs IoT** : L'intégration de nouveaux capteurs (humidité, pression, luminosité, etc.) permettrait d'élargir les cas d'utilisation de l'API, en offrant des données encore plus riches et variées.
    
2. **Amélioration de l’interface utilisateur** : Actuellement, l'API retourne des données sous forme brute. Le projet pourrait inclure une interface graphique ou un dashboard pour visualiser ces données en temps réel, ce qui rendrait l'application plus accessible aux utilisateurs finaux.
    
3. **Gestion avancée des tokens** :
    
    - **Expiration et renouvellement des tokens** : Implémentation d'une gestion automatique des tokens avec expiration et renouvellement pour garantir une sécurité continue. Cela pourrait inclure des mécanismes pour régénérer les tokens OAuth2 avant qu'ils n'expirent.
    - **Révocation des tokens** : Implémentation de la possibilité de révoquer un token en cas de besoin, pour ajouter un niveau de contrôle supplémentaire en cas de compromission ou de changement de permissions.
4. **Déploiement en environnement de production** : Une fois les fonctionnalités avancées mises en place, le système pourrait être déployé dans un environnement de production, où des exigences supplémentaires en termes de robustesse et de disponibilité seraient prises en compte (ex. : mise en place de backups, redondance des services).
    

En somme, ce projet ouvre la voie à de nombreuses améliorations et extensions, tout en garantissant une architecture sécurisée et évolutive pour la gestion des capteurs IoT.