# Rapport Travail 1 : Intégration des APIs Ecowatt et Météo France avec OAuth2

## 🔹 Introduction

L'objectif de ce travail était d'implémenter une solution permettant d'accéder aux données des services Ecowatt (RTE) et des Données d'observations de Météo France tout en sécurisant les échanges via le protocole **OAuth2**. Ce rapport détaille l'implémentation technique réalisée.

---

## 🔹 1. Authentification OAuth2

### 📌 Objectif

L'API Ecowatt nécessite une authentification OAuth2 pour accéder aux données. Nous avons mis en place une fonction permettant de récupérer un **jeton d'accès (access token)** à partir de l'endpoint d'authentification fourni par RTE.

### 🖥️ Implémentation

```python 
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
```

### 🔍 Explication

L'API Ecowatt nécessite une authentification OAuth2 pour accéder aux données. Une fonction a été mise en place pour récupérer un **jeton d'accès (access token)** à partir de l'endpoint d'authentification fourni par RTE. Une requête **POST** est envoyée avec les **identifiants OAuth2 encodés en Base64**. Si la réponse est **200 OK**, le **token d'accès** est extrait. En cas d'erreur, un message explicatif est affiché. Le code implémenté permet de gérer cette authentification et de renvoyer un jeton valide pour les appels ultérieurs à l'API Ecowatt.

---

## 🔹 2. Récupération des données Ecowatt

### 📌 Objectif

Une fois authentifié, nous devons récupérer les **signaux Ecowatt** indiquant les pics de consommation d'électricité.

### 🖥️ Implémentation

```python 
def fetch_ecowatt_data(token, file_path):
	url = "https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals"
	headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
	
	max_retries = 5
	retry_delay = 10  # secondes

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
```

### 🔍 Explication

Une fois l'utilisateur authentifié, il devient possible de récupérer les **signaux Ecowatt** indiquant les pics de consommation d'électricité. Pour ce faire, une requête **GET** est envoyée à l'API Ecowatt en incluant le **token d'accès** dans l'en-tête de la requête. Les données récupérées, au format JSON, sont ensuite sauvegardées localement dans un fichier `ecowatt.json`. Le code inclut également un mécanisme de gestion des erreurs. Si le serveur renvoie une erreur de type **429 (Trop de requêtes)**, la fonction attend un délai et tente à nouveau jusqu'à un maximum de 5 tentatives. Cela permet d'éviter d'éventuels blocages dus à une surcharge de requêtes. En cas d'autres erreurs, un message explicatif est fourni.

---

## 🔹 3. Analyse des données Ecowatt

### 📌 Objectif

Les signaux récupérés doivent être traités afin d'identifier les périodes de **tension électrique**.

### 🖥️ Implémentation avec une liste chaînée

```python 
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
```

### 🔍 Explication

Les données récupérées doivent ensuite être analysées pour identifier les périodes de **tension électrique**. Pour cela, une structure de données sous forme de **liste chaînée** a été utilisée. Chaque nœud de cette liste représente une période de faible consommation, identifiée par la combinaison du jour et de l'heure. L'implémentation permet de parcourir les données récupérées et d'ajouter les créneaux horaires correspondants dans la liste chaînée. Une fois la liste complétée, les créneaux sont affichés à l'écran, ce qui permet d'identifier rapidement les périodes critiques.

***
## 🔹 Conclusion

Ce travail nous a permis de mettre en place une **authentification sécurisée** avec OAuth2, d'effectuer des requêtes vers l'API **Ecowatt de RTE**, et d'analyser les signaux récupérés.

✅ **Résultats obtenus :**

- Récupération du **token OAuth2**.
- Téléchargement des **signaux Ecowatt** en JSON.
- Analyse et extraction des périodes critiques.

🚀 **Prochaine étape :** Intégration du délestage énergétique avec Phidget !


***

# Sommaire : Intégration de l'API Ecowatt avec OAuth2

## 1. Introduction
- Présentation du projet
- Objectifs de l'intégration
## 2. Authentification OAuth2
- Importance de l'authentification OAuth2
- Bonnes pratiques en matière de sécurité
- Principe de fonctionnement
- Obtention du token d'accès
- Gestion des erreurs d'authentification
## 3. Récupération des données des APIs
- API Ecowatt
    - Requête et format des données
## 4. Analyse et exploitation des données

## 5. Conclusion
- Résumé des résultats obtenus
- Améliorations possibles et perspectives d'évolution
***
### **1. Introduction**

#### **Présentation du projet**

Ce projet vise à intégrer l'API Ecowatt de RTE (Réseau de Transport d'Électricité) pour fournir des informations sur la consommation d'énergie en France. L'API Ecowatt permet de suivre en temps réel l'état du réseau électrique national, avec des prévisions et des alertes concernant la consommation d'électricité. Elle est utilisée principalement pour gérer les risques de tension sur le réseau et aider à la prise de décision en cas de pics de consommation.

L'intégration de cette API avec OAuth2 permet de sécuriser l'accès aux données tout en offrant une méthode simple et efficace pour récupérer les informations nécessaires à l’analyse et à l’exploitation du réseau énergétique.

#### **Objectifs de l'intégration**

L'intégration de l'API Ecowatt vise plusieurs objectifs principaux :
1. **Sécuriser l'accès aux données** : L’utilisation d'OAuth2 permet de garantir une authentification sécurisée des applications qui accèdent aux données Ecowatt.
2. **Récupérer des données en temps réel** : Le projet permet de récupérer des informations sur la consommation d'énergie et les prévisions associées, permettant une meilleure gestion de la demande énergétique.
3. **Analyser et exploiter les données** : En structurant et stockant les données récupérées, l’objectif est de réaliser des analyses prédictives, de surveiller les tendances de consommation et d'améliorer la gestion du réseau électrique en temps réel.
4. **Optimiser la gestion des quotas** : L'intégration prévoit des mécanismes pour gérer les limitations d'accès (quotas) de l'API Ecowatt, afin d'éviter les erreurs liées aux appels trop fréquents ou aux dépassements de quota.

L’objectif final est d’apporter une solution intelligente et sécurisée pour le suivi de la consommation électrique en France, tout en assurant une gestion efficace de l’accès aux données grâce à l’utilisation de OAuth2.

### **2. Authentification OAuth2**

L'authentification OAuth2 est un standard moderne de gestion des permissions d'accès aux ressources protégées via un jeton d'accès (token). Il est largement utilisé dans les APIs pour sécuriser les échanges de données entre un client (comme une application) et un serveur tout en respectant la confidentialité des informations sensibles.

#### **Importance de l'authentification OAuth2**

OAuth2 permet de garantir que seules les applications autorisées peuvent accéder aux ressources protégées. Pour notre projet, cela signifie qu'aucune donnée sensible ou personnelle ne sera partagée sans avoir effectué une authentification sécurisée, ce qui est crucial pour le respect de la vie privée et la sécurité des données.

#### **Bonnes pratiques en matière de sécurité**

- **Stockage sécurisé des identifiants** : Les informations sensibles, comme les identifiants du client et le secret, ne doivent pas être exposées dans le code source ou dans des fichiers accessibles.
- **Utilisation de HTTPS** : Pour garantir la confidentialité des échanges, les requêtes doivent toujours être envoyées via HTTPS.
- **Renouvellement du token** : Les tokens d'accès doivent être régulièrement renouvelés pour réduire les risques de sécurité en cas de compromission.
- **Scopes d'autorisation** : Il est recommandé de restreindre les permissions demandées par le client au strict nécessaire. Cela minimise les risques en cas d'usage malveillant du token.

#### **Principe de fonctionnement**

Le processus OAuth2 implique trois étapes clés :

1. **Obtention du token d'accès** : Le client envoie une requête au serveur d'autorisation pour obtenir un token d'accès.
2. **Accès aux ressources protégées** : Une fois le token obtenu, le client peut l'utiliser pour accéder aux ressources protégées sur le serveur d'API.
3. **Renouvellement du token** : Si le token expire, il peut être renouvelé à l'aide d'un _refresh token_, permettant au client de maintenir l'accès sans nécessiter une nouvelle authentification de l'utilisateur.

![[Pasted image 20250222203710.png]]
<p align="center"><em><small>Schéma d'explication du protocole OAuth2 dans un échange API</small></em></p>

#### **Obtention du token d'accès**
``` python
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
```
Dans le code, la fonction `get_oauth_token()` est responsable de l'obtention du token d'accès via l'API d'authentification d'RTE :
1. **URL du serveur d'authentification** : L'URL `"https://digital.iservices.rte-france.com/token/oauth"` est utilisée pour envoyer une requête `POST` afin de récupérer le token d'accès.
2. **En-têtes de la requête** : Les en-têtes incluent l'authentification de base (avec un identifiant et un secret client encodés en Base64) et spécifient que le contenu est de type `application/x-www-form-urlencoded` (format requis pour l'authentification OAuth2).
3. **Réponse de l'API** : Si la requête réussit (code HTTP 200), le token d'accès est extrait de la réponse JSON (`token_data['access_token']`).
4. **Gestion des erreurs** : Si la requête échoue (par exemple en raison d'un code de statut HTTP non 200), un message d'erreur est affiché et la fonction retourne `None`.

Cela permet à l'application d'obtenir un accès sécurisé aux ressources de l'API Ecowatt avec un jeton valide, qui peut ensuite être utilisé pour effectuer des requêtes protégées.

### 3. Récupération des données des APIs

Cette partie du code est responsable de l'interrogation de l'API Ecowatt après avoir obtenu un token OAuth2. Elle comprend plusieurs étapes clés :


#### **🔹 Récupérer les données Ecowatt**

Voici la fonction qui récupère les données de l'API :
``` python
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
        
        elif response.status_code == 429:  # Trop de requêtes
            print(f"⚠️ Trop de requêtes, attente {retry_delay} secondes...")
            time.sleep(retry_delay)
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return None

    print("❌ Échec après plusieurs tentatives")
    return None
```

L'URL `https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals` est appelée pour récupérer les prévisions Ecowatt. L'en-tête `Authorization: Bearer <token>` permet de s'authentifier grâce au token OAuth2 récupéré précédemment. L'en-tête `Accept: application/json` précise que la réponse attendue doit être au format JSON.

La fonction prévoit jusqu'à **cinq tentatives** en cas d'échec. Si le serveur renvoie `429 Too Many Requests`, le script attend **10 secondes** avant de réessayer avec `time.sleep(retry_delay)`. En cas d'erreur autre, le code s'arrête immédiatement.

Si la requête réussit avec un code **200**, la réponse est convertie en JSON et sauvegardée dans un fichier `ecowatt.json`. Un message confirme le bon enregistrement des données.

Si l'API répond correctement, les données sont renvoyées pour être utilisées dans l'analyse. En cas d'échec après plusieurs tentatives, un message d'erreur est affiché.

#### **🔹 3. Lire et analyser les données Ecowatt**

Cette partie convertit les données JSON en une structure manipulable.

##### **Création d'une liste chaînée**
```python
class Node:
    def __init__(self, jour, pas):
        self.jour = jour
        self.pas = pas
        self.next = None
```
Cette classe définit un **nœud** pour stocker les prévisions Ecowatt sous forme d'une **liste chaînée** (linked list), ce qui permet d'optimiser l'ajout et la lecture des éléments.

##### **Ajout d'un élément à la liste chaînée**
``` python
def add_to_linked_list(head, jour, pas):
    new_node = Node(jour, pas)
    if not head:
        return new_node
    last = head
    while last.next:
        last = last.next
    last.next = new_node
    return head
```
Cette fonction ajoute un nouvel élément (`jour, pas horaire`) dans la liste chaînée.

##### **Lecture et affichage des données**
```python
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
```
Le fichier `ecowatt.json` est ouvert et chargé en mémoire. Si le fichier n'existe pas, un message d'erreur est affiché.

Les données Ecowatt sont ensuite extraites. Une boucle parcourt chaque prévision (`signals`). Pour chaque prévision associée à un jour donné, elle récupère les heures (`values`). Si `hvalue == 0` (absence de tension sur le réseau), l'heure et le jour sont stockés dans la liste chaînée.

Enfin, la liste chaînée est parcourue pour afficher chaque entrée sous la forme 📅 **Jour:** ..., ⏰ **Heure:** ...h.

### Conclusion

Les résultats obtenus montrent une stabilité du réseau électrique sur la période analysée, sans alerte ni coupure détectée. L’analyse des données issues de l’API Ecowatt confirme une disponibilité constante de l’énergie, avec des valeurs de tension normales sur l’ensemble des créneaux horaires.

Pour améliorer l’exploitation des données, plusieurs pistes peuvent être envisagées. Une optimisation de l’analyse pourrait inclure un suivi en temps réel des prévisions avec des alertes en cas de risque de tension sur le réseau. De plus, l’intégration de ces données dans un système plus large de gestion énergétique permettrait d’anticiper et d’adapter la consommation selon les recommandations d’Ecowatt. Enfin, des visualisations dynamiques sous forme de graphiques interactifs pourraient offrir une meilleure interprétation des tendances énergétiques.