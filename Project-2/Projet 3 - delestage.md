**Sommaire**

1. **Introduction**
    - 1.1 Contexte du projet
    - 1.2 Objectifs du projet
    - 1.3 Importance de la gestion de la consommation énergétique
2. **Matériel et Technologies**
    - 2.1 Phidget Interface Kit 0/0/8 (P/N 1017)
        - 2.1.1 Caractéristiques techniques
        - 2.1.2 Utilisation dans le projet
    - 2.2 LED et relais
        - 2.2.1 Fonctionnement des relais
        - 2.2.2 Rôle des LED dans la simulation de délestage
    - 2.4 Outils de développement
        - 2.4.1 Phidget22 pour Python
        - 2.4.2 Autres outils et bibliothèques utilisées (par exemple, Requests, JSON)
3. **Implémentation Logicielle**
    - 4.1 Récupération des données de consommation via l'API Ecowatt
        - 4.1.1 Méthode HTTP GET
        - 4.1.2 Structure de la réponse JSON
        - 4.1.3 Analyse des données pour identifier les périodes de forte consommation
    - 4.2 Contrôle des relais
        - 4.2.1 Utilisation de la bibliothèque Phidget22
        - 4.2.2 Logique de commutation des relais en fonction des données de consommation
4. **Conclusion**
    - 8.1 Récapitulatif des objectifs atteints
    - 8.2 Impact du projet sur la gestion énergétique
    - 8.3 Perspectives d’évolution du projet
***

### **1. Introduction**

#### **1.1 Contexte du projet**

La gestion de la consommation énergétique est un enjeu majeur à l’heure où la transition énergétique devient une priorité mondiale. La demande en électricité varie au cours de la journée, atteignant des pics de consommation qui sollicitent fortement le réseau électrique. Ces fluctuations peuvent engendrer des risques de surcharge, nécessitant des ajustements de production parfois coûteux et polluants.

Afin de répondre à ces défis, des solutions de gestion de la consommation ont été développées, notamment par le biais de mécanismes de délestage énergétique. Le délestage consiste à réduire la consommation d’énergie en désactivant temporairement certains équipements non essentiels lors des périodes de forte demande. Ce principe est particulièrement pertinent dans les environnements où la maîtrise des coûts et de l’empreinte carbone est une priorité, que ce soit dans le cadre domestique, industriel ou institutionnel.

Dans ce contexte, le projet présenté vise à expérimenter un système de délestage basé sur l’utilisation du **Phidget Interface Kit 0/0/8 (P/N 1017)**, un module permettant de piloter des relais pour activer ou désactiver des charges électriques. Les décisions de délestage seront prises en fonction des signaux de consommation fournis par l’**API Ecowatt de RTE**, qui fournit des prévisions sur l’état du réseau électrique.

L’intégration de l’authentification sécurisée **OAuth2** pour accéder à l’API Ecowatt et la programmation en **Python** pour piloter les relais permettent d’automatiser le processus et d’offrir une solution flexible et évolutive.

#### **1.2 Objectifs du projet**

Le projet a pour objectif principal de **concevoir et mettre en place un système de délestage énergétique** basé sur les données de consommation fournies par l’API Ecowatt. Plus précisément, il vise à :

1. **Récupérer les signaux de consommation énergétique** via l’API Ecowatt en utilisant un système d’authentification sécurisé (**OAuth2**).
2. **Analyser ces données** pour détecter les périodes de forte demande en électricité.
3. **Automatiser le délestage** en activant ou désactivant des relais connectés à des LED simulant des appareils énergivores.

En parallèle, ce projet permettra de renforcer des compétences techniques en programmation, en gestion d’API, en manipulation de **Phidgets** et en mise en place d’un **protocole de communication sécurisé**.

#### **1.3 Importance de la gestion de la consommation énergétique**

La consommation énergétique est un enjeu crucial à plusieurs niveaux :

- **Économique** : La réduction de la consommation d’énergie lors des pics permet d’éviter des coûts supplémentaires liés à l’utilisation d’unités de production moins performantes et plus onéreuses.
- **Environnemental** : Une gestion efficace de la demande réduit la nécessité de recourir à des sources d’énergie fossiles pour répondre aux pics de consommation, limitant ainsi les émissions de gaz à effet de serre.
- **Réglementaire** : De nombreux gouvernements encouragent ou imposent des stratégies de réduction de la consommation, notamment via des incitations à l’effacement de la demande (délestage volontaire des entreprises et particuliers).
- **Technique** : Un réseau mieux équilibré est plus stable, limitant ainsi les risques de surcharge, de panne généralisée (black-out) et améliorant la fiabilité globale de l’alimentation électrique.

Le projet s’inscrit donc dans une démarche **d’optimisation énergétique**, apportant une solution pratique qui pourrait être appliquée à des contextes plus larges, tels que les **systèmes de domotique intelligents** ou les **réseaux industriels** souhaitant optimiser leur consommation en fonction de la demande globale.

### **2. Matériel et Technologies**

Dans cette section, nous présentons les équipements et technologies utilisés dans le projet. Le matériel sélectionné doit permettre un **contrôle efficace des charges électriques** tout en assurant une **interopérabilité avec les systèmes numériques** pour la gestion des données de consommation.

#### **2.1 Phidget Interface Kit 0/0/8 (P/N 1017)**

Le **Phidget Interface Kit 0/0/8** est une carte d'interface permettant de contrôler **jusqu'à huit relais électromécaniques** via une connexion **USB**. Il est conçu pour piloter des charges électriques, ce qui en fait un élément clé du système de délestage énergétique.

##### **2.1.1 Caractéristiques techniques**

Les principales caractéristiques techniques du Phidget Interface Kit 0/0/8 sont les suivantes :

- **Type de relais** : DPDT (Double Pole Double Throw) électromécaniques
- **Nombre de relais** : 8
- **Tension de commutation** :
    - **Jusqu’à 250V AC (2A max)**
    - **Jusqu’à 200V DC (2A max)**
- **Puissance maximale** : 60W
- **Interface de communication** : USB
- **Isolation galvanique** : Protection entre l’électronique et la charge commutée
- **Indicateurs LED** : Affichage de l’état de chaque relais (ON/OFF)
- **Compatibilité logicielle** : Prise en charge par plusieurs langages de programmation (Python, C++, Java, etc.) grâce à la bibliothèque **Phidget22**

Le choix de ce module repose sur plusieurs critères :

1. **Simplicité d’intégration** avec un ordinateur ou un microcontrôleur via USB.
2. **Fiabilité des relais électromécaniques**, permettant de commuter des charges variées (appareils électriques, LED, moteurs, etc.).
3. **Flexibilité d’utilisation**, avec huit canaux indépendants pour contrôler plusieurs circuits simultanément.
4. **Interopérabilité avec Python**, facilitant l'automatisation du délestage en fonction des données Ecowatt.

##### **2.1.2 Utilisation dans le projet**

Dans notre projet, le **Phidget Interface Kit 0/0/8** est utilisé pour **simuler le contrôle des appareils énergivores** à l’aide de LED. Son fonctionnement repose sur l’activation ou la désactivation des relais en réponse aux **signaux de consommation énergétique** fournis par l’API **Ecowatt**.

Voici le principe de fonctionnement dans notre système :

1. **Récupération des signaux de consommation** via l’API Ecowatt (indiquant les périodes de forte demande en électricité).
2. **Analyse des données** :
    - Si la demande est élevée (**hvalue > 1**), un ou plusieurs relais sont activés pour couper certains appareils (simulation par LED).
    - Si la consommation est normale, les relais restent désactivés, laissant les LED allumées.
3. **Commande des relais** via le Phidget Interface Kit, en utilisant la bibliothèque **Phidget22** sous Python.
4. **Affichage de l’état des LED** pour représenter visuellement le fonctionnement du délestage.

**Exemple de connexion** :

- Chaque LED est branchée entre **la borne COM et la borne NO** du relais.
- Lorsqu’un relais est activé, le circuit est fermé et la LED s’allume (indiquant que l’appareil est en fonctionnement).
- Lorsqu’un relais est désactivé, le circuit est ouvert et la LED s’éteint (simulant l’arrêt d’un appareil pour économiser l’énergie).

Le **Phidget Interface Kit 0/0/8** joue donc un rôle central dans l’expérimentation de ce projet en permettant **une gestion dynamique des charges électriques**, à la manière d’un système de délestage réel appliqué à des équipements domestiques ou industriels.

### **2.2 LED et Relais**

Dans ce projet, l’utilisation des **relais** et des **LED** permet de simuler le fonctionnement d’un système de **délestage énergétique**. Les relais jouent le rôle d’interrupteurs contrôlés électroniquement, tandis que les LED servent d’indicateurs visuels pour représenter l’activation ou la désactivation des appareils énergivores.

#### **2.2.1 Fonctionnement des relais**

Un **relais** est un **dispositif électromécanique** qui permet d’ouvrir ou de fermer un circuit électrique en fonction d’un signal de commande. Le **Phidget Interface Kit 0/0/8** utilisé dans ce projet comporte **huit relais DPDT** (Double Pole Double Throw), qui peuvent commuter des charges sous des tensions alternatives (AC) ou continues (DC).

##### **Principe de fonctionnement d’un relais**

Un relais est constitué de deux parties principales :

- **La bobine électromagnétique** : Lorsque celle-ci est alimentée, elle génère un champ magnétique qui actionne un mécanisme mécanique interne.
- **Le contacteur (switch interne)** : Il permet de commuter l’état du circuit en fonction de l’état de la bobine.

Chaque relais dispose de trois bornes essentielles :

- **COM (Common)** : Borne commune du relais.
- **NC (Normally Closed)** : Circuit fermé lorsque le relais est **au repos**.
- **NO (Normally Open)** : Circuit ouvert lorsque le relais est **au repos**.

Lorsque la bobine du relais est activée :  
✅ Le contact **NC s’ouvre**, interrompant l’alimentation d’un circuit.  
✅ Le contact **NO se ferme**, permettant l’alimentation d’un circuit.

Dans notre projet, chaque relais est utilisé pour **simuler l’arrêt ou l’activation d’un appareil électrique** en fonction des signaux de consommation énergétique fournis par l’API **Ecowatt**.

#### **2.2.2 Rôle des LED dans la simulation de délestage**

Les **LED** sont utilisées pour représenter visuellement l’état des appareils énergivores. Elles permettent de simuler un fonctionnement **réaliste** du système de délestage :

- **LED allumée** 🔴 → L’appareil est en fonctionnement, consommant de l’énergie.
- **LED éteinte** ⚫ → L’appareil est mis en veille ou arrêté pour réduire la consommation énergétique.

##### **Schéma de connexion LED - Relais**

Chaque LED est connectée au **relais correspondant** selon le schéma suivant :

- **Anode (+) de la LED** connectée à **la borne COM du relais**.
- **Cathode (-) de la LED** reliée à une **résistance** (pour limiter le courant) et ensuite à la **masse (GND)**.
- **Alimentation 5V** fournie à la borne NO du relais.

Lorsque le relais est activé (forte consommation énergétique détectée) :  
✅ Le contact NO se ferme → **La LED s’éteint**, indiquant que l’appareil est **coupé** pour économiser l’énergie.

Lorsque le relais est désactivé (consommation normale) :  
✅ Le contact NO s’ouvre → **La LED s’allume**, indiquant que l’appareil **fonctionne normalement**.

Grâce à cette simulation, nous pouvons observer en temps réel **comment le système de délestage réagirait dans un environnement réel**, en **activant ou désactivant des charges en fonction des signaux de consommation énergétique** fournis par l’API Ecowatt.

### **2.4 Outils de Développement**

Le développement du projet repose sur plusieurs outils et bibliothèques permettant **d’interagir avec le Phidget Interface Kit, de récupérer les données de l’API Ecowatt et de les traiter**.

#### **2.4.1 Phidget22 pour Python**

La bibliothèque **Phidget22** est une API permettant de **contrôler les modules Phidget** en Python. Elle est essentielle pour gérer les **relais** du Phidget Interface Kit 0/0/8.

##### **Installation de Phidget22**

Avant d’utiliser la bibliothèque, il faut l’installer avec :
```cmd
pip install Phidget22
```

**Exemple de contrôle d’un relais avec Phidget22**
```python
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *

# Création de l’objet DigitalOutput pour un relais
relay = DigitalOutput()

# Définition du port du Phidget Interface Kit
relay.setHubPort(0)
relay.setIsHubPortDevice(True)

# Connexion au relais
relay.openWaitForAttachment(1000)

# Activation du relais (mise sous tension)
relay.setState(True)

# Pause pour observer l’état du relais
import time
time.sleep(2)

# Désactivation du relais (coupure de l’appareil)
relay.setState(False)

# Fermeture de la connexion avec le relais
relay.close()
```

Dans cet exemple, on **active** le relais pendant **2 secondes**, puis on le **désactive**, simulant ainsi un **délestage temporaire d’un appareil électrique**.

---

### **2.4.2 Bibliothèques utilisées**

Dans notre projet, nous utilisons plusieurs **bibliothèques Python** pour assurer la communication avec l’API Ecowatt, le contrôle du Phidget Interface Kit et la gestion de l’API FastAPI qui permet d’exposer les fonctionnalités du système.

|**Bibliothèque**|**Utilisation**|
|---|---|
|`fastapi`|Framework web permettant de créer une API REST pour interagir avec le système de délestage.|
|`HTTPException` (FastAPI)|Gestion des erreurs HTTP pour renvoyer des réponses claires en cas de problème.|
|`CORSMiddleware` (FastAPI)|Autorise les requêtes provenant de différentes origines (Cross-Origin Resource Sharing).|
|`json`|Manipulation des données JSON, notamment celles issues de l’API Ecowatt.|
|`os`|Gestion des variables d’environnement et des fichiers système.|
|`requests`|Envoi de requêtes HTTP à l’API Ecowatt pour récupérer les prévisions énergétiques.|
|`time`|Gestion des temporisations pour éviter des changements trop fréquents d’état des relais.|
|`datetime`|Traitement des dates et heures pour analyser les périodes de forte consommation.|
|`Phidget22.Devices.DigitalOutput`|Contrôle des relais du Phidget Interface Kit 0/0/8.|

#### **Installation des bibliothèques**

Toutes ces bibliothèques peuvent être installées avec **pip** :
``` cmd
pip install fastapi requests phidget22
```
Certaines bibliothèques comme **json, os, time et datetime** sont des modules standards de Python et n’ont pas besoin d’être installées séparément.

#### **Exemple d’utilisation des bibliothèques dans le projet**

##### **1️⃣ Création d’une API avec FastAPI**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuration du middleware CORS pour accepter les requêtes de n'importe quelle origine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API de gestion du délestage énergétique"}
```

Dans cet exemple, nous créons une **API REST** avec **FastAPI**, permettant d’accéder au système via des requêtes HTTP. Le middleware **CORS** est utilisé pour autoriser les requêtes provenant d’autres origines.

---

##### **2️⃣ Récupération des données Ecowatt avec `requests` et `json`**
```python
import requests
import json

def fetch_ecowatt_data(token):
    url = "https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
```

Ici, la bibliothèque **requests** est utilisée pour interroger l’API Ecowatt, et **json** sert à **analyser la réponse en format JSON**.

---

##### **3️⃣ Gestion des relais avec `Phidget22.Devices.DigitalOutput`**

```python
from Phidget22.Devices.DigitalOutput import DigitalOutput

def control_relay(channel, state):
    relay = DigitalOutput()
    relay.setHubPort(channel)
    relay.setIsHubPortDevice(True)
    
    relay.openWaitForAttachment(1000)
    relay.setState(state)
    relay.close()
```
Cette fonction utilise **Phidget22** pour contrôler les relais du **Phidget Interface Kit 0/0/8**, en activant ou désactivant un relais spécifique.

---

##### **4️⃣ Utilisation des modules `time`, `datetime` et `os`**
```python
import time
from datetime import datetime
import os

# Exemple d'attente pour éviter un basculement trop rapide des relais
time.sleep(1)

# Récupération de l’heure actuelle pour analyser la consommation énergétique
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Chargement du token d’authentification depuis une variable d’environnement
api_token = os.getenv("ECOWATT_TOKEN", "default_token")
```
Ici, **time** permet d’introduire une pause entre deux changements d’état des relais, **datetime** est utilisé pour gérer les timestamps des signaux Ecowatt, et **os** permet de récupérer des variables d’environnement pour sécuriser les données sensibles comme les tokens API.

### **Conclusion**

L’utilisation combinée de ces bibliothèques permet d’avoir un système **modulaire, performant et sécurisé** pour la gestion du délestage énergétique.

✅ **FastAPI** pour exposer une API REST et faciliter l’interaction avec le système.  
✅ **Requests & JSON** pour interroger l’API Ecowatt et traiter les prévisions énergétiques.  
✅ **Phidget22** pour contrôler les relais du Phidget Interface Kit.  
✅ **Time & Datetime** pour synchroniser les actions avec les heures de forte consommation.  
✅ **OS** pour gérer les paramètres système et éviter d’exposer des informations sensibles dans le code.

Cette architecture assure un fonctionnement **fluide et évolutif**, avec la possibilité d'ajouter de nouvelles fonctionnalités comme la gestion **multi-appareils** ou l’intégration d’autres sources de données énergétiques.

---

### **4. Implémentation Logicielle**

L’implémentation logicielle du projet repose sur l'utilisation de plusieurs composants qui interagissent entre eux pour récupérer les données de consommation, gérer l’état des relais et ajuster la consommation en temps réel. Ce processus est guidé par l'API Ecowatt de RTE, qui fournit des informations détaillées sur les périodes de forte consommation électrique.

#### **4.1 Récupération des données de consommation via l'API Ecowatt**

##### **4.1.1 Méthode HTTP GET**

L'API Ecowatt permet de récupérer les données de consommation via une requête HTTP GET. Cette requête est envoyée au serveur d’RTE pour obtenir des données sous forme de JSON. Nous utilisons la méthode suivante pour envoyer la requête :
```python
def fetch_ecowatt_data():
    token = get_oauth_token()  # Fonction pour obtenir un token OAuth valide
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(ECOWATT_URL, headers=headers)  # Requête GET

    if response.status_code == 200:
        data = response.json()
        with open(ECO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return data
    raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des données Ecowatt")
```
Cette fonction interroge l'API Ecowatt et récupère les données de consommation en fonction du jour et de l’heure. Ces données sont ensuite stockées dans un fichier local (`ecowatt.json`), afin de pouvoir être traitées ultérieurement.

##### **4.1.2 Structure de la réponse JSON**

Les données récupérées de l'API sont structurées en JSON, avec les informations suivantes :

- **signals** : Contient les signaux de consommation pour différents jours.
- **values** : Indique l’intensité de la consommation à différents moments de la journée sous forme de "pas" horaires.
- **hvalue** : Représente la valeur de consommation (0 pour une consommation normale, 1 pour une forte consommation nécessitant un délestage).

Exemple de structure JSON :
```json
{
  "signals": [
    {
      "jour": "2025-02-23",
      "values": [
        {"pas": 0, "hvalue": 0},
        {"pas": 1, "hvalue": 1},
        {"pas": 2, "hvalue": 0},
        ...
      ]
    }
  ]
}
```
##### **4.1.3 Analyse des données pour identifier les périodes de forte consommation**

L’analyse des données de consommation permet de détecter les périodes de forte consommation, marquées par un `hvalue` égal à 1. Ces périodes nécessitent un délestage, et nous ajustons en conséquence l’état des relais pour réduire la consommation. Le code suivant permet de détecter ces périodes :
```python
def analyze_ecowatt_data(data):
    critical_periods = []

    if data:
        for signal in data.get("signals", []):
            jour = signal["jour"]
            for entry in signal.get("values", []):
                heure = entry["pas"]
                niveau = entry["hvalue"]
                
                if niveau == 1:  # Seulement les périodes nécessitant un délestage
                    critical_periods.append((jour, heure))

    return critical_periods
```
Ainsi, une fois que les périodes critiques ont été détectées, nous pouvons ajuster l'état des relais en conséquence.

#### **4.2 Gestion des relais via l’Interface Phidget**

L'interface Phidget permet de contrôler les relais en fonction des données analysées. Lorsqu'une période de forte consommation est détectée (hvalue = 1), l'état des relais est modifié pour effectuer un délestage.

Le code suivant permet de contrôler les relais en fonction de l’état des périodes critiques :
```python
@app.get("/get_relays_state")
def get_relays_state():
    global relay_states  # Modifie l'état des relais à l'échelle globale

    try:
        with open(ECO_FILE, "r") as f:
            data = json.load(f)

        today = datetime.now().strftime("%Y-%m-%d")
        signal = next((s for s in data.get("signals", []) if s.get("jour", "").startswith(today)), None)

        if not signal:
            return relay_states  # Retourne l'état actuel si aucune donnée trouvée

        current_hour = datetime.now().hour
        value = next((v for v in signal.get("values", []) if v.get("pas") == current_hour), None)

        if value is None:
            return relay_states  # Retourne l'état actuel si pas de donnée 'hvalue' trouvée

        new_state = bool(value.get("hvalue", 0))  # Si hvalue est 1, délestage activé

        if relay_states[1] != new_state:  # Si l'état du relais change
            relay_states[1] = new_state
            if 1 in relays and relays[1].getAttached():
                relays[1].setState(new_state)
                print(f"🔄 Relais 1 mis à {'ON' if new_state else 'OFF'} à {current_hour}h.")
            else:
                print("⚠️ Relais 1 non attaché ou inaccessible.")

    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture du fichier EcoWatt : {e}")

    return relay_states  # Retourne l'état mis à jour des relais
```
Dans cet exemple, le relais 1 est activé ou désactivé en fonction de la valeur de `hvalue` pour l'heure actuelle.

#### **4.3 Mise à jour des données (hvalue)**

Les données peuvent être mises à jour manuellement si nécessaire. Le code suivant permet de modifier la valeur de `hvalue` pour une période donnée :
```python
@app.post("/update_hvalue")
def update_hvalue(data: dict):
    signal = data.get("signal")
    pas = data.get("pas")
    hvalue = data.get("hvalue")
    if not os.path.exists(ECO_FILE):
        raise HTTPException(status_code=404, detail="Fichier Ecowatt introuvable")

    with open(ECO_FILE, "r") as f:
        data = json.load(f)
        
    for signal_data in data.get("signals"):
        if signal_data.get("jour") == signal:
            for value in signal_data.get("values"):
                if str(value.get("pas")) == pas:
                    value["hvalue"] = hvalue  # Met à jour le hvalue

    try:
        with open(ECO_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier : {e}")

    get_relays_state()
    return {"message": "hvalue mis à jour", "signal": signal, "pas": pas, "hvalue": hvalue}
```
Cela permet de mettre à jour manuellement le `hvalue` pour des périodes spécifiques, et ainsi d’ajuster immédiatement l’état des relais si nécessaire.

### **4. Conclusion**

Le projet de délestage énergétique avec le système de relais et l'API Ecowatt de RTE a permis de développer une solution complète pour la gestion dynamique de la consommation d'énergie en fonction des périodes de forte demande. L'implémentation logicielle et matérielle a montré une interaction fluide entre l'acquisition des données en temps réel et le contrôle des relais.

#### **8.1 Récapitulatif des objectifs atteints**

Les principaux objectifs du projet ont été atteints avec succès :

- **Récupération des données de consommation** : L’intégration de l’API Ecowatt a permis de récupérer des informations sur la consommation d'énergie en temps réel, et de les stocker pour analyse.
- **Analyse des périodes critiques** : En analysant les périodes de forte consommation, le système peut détecter les moments où des actions de délestage sont nécessaires.
- **Contrôle des relais** : En fonction des données récupérées, le système ajuste l'état des relais pour délester les équipements non essentiels pendant les périodes de forte demande.
- **Mise à jour manuelle des données** : La possibilité de mettre à jour les valeurs de consommation (`hvalue`) manuellement a été implémentée, offrant ainsi une flexibilité dans la gestion de la consommation.

#### **8.2 Impact du projet sur la gestion énergétique**

Le projet a eu un impact direct sur l'optimisation de la gestion énergétique en permettant un ajustement en temps réel de la consommation. Grâce à l'automatisation du délestage des équipements non essentiels, il devient possible de :

- **Réduire la consommation pendant les périodes critiques** : En désactivant des relais en cas de forte demande, on réduit les pics de consommation, ce qui peut contribuer à une meilleure répartition de l'énergie sur le réseau.
- **Minimiser les coûts énergétiques** : En concentrant la consommation sur des périodes où la demande est plus faible, le système peut contribuer à diminuer les coûts associés à des tarifs énergétiques plus élevés pendant les heures de pointe.
- **Optimisation des ressources** : Le système permet de gérer l'énergie de manière plus rationnelle, en activant uniquement les équipements essentiels pendant les périodes de haute consommation.

#### **8.3 Perspectives d’évolution du projet**

Le projet peut être amélioré et étendu dans plusieurs directions pour offrir davantage de fonctionnalités et de flexibilité :

1. **Intégration avec d'autres systèmes de gestion d'énergie** : Il serait intéressant de connecter le système à d’autres plateformes de gestion énergétique ou à des outils de surveillance supplémentaires pour une meilleure analyse prédictive de la consommation.
    
2. **Prévision de la consommation** : L’ajout de modèles d’apprentissage automatique pourrait permettre de prédire les périodes de forte consommation à l’avance, en se basant sur les tendances historiques et d'autres facteurs, ce qui permettrait un délestage anticipé.
    
3. **Gestion multizone** : Le système pourrait être étendu pour gérer des zones géographiques multiples ou des bâtiments différents, chacun avec ses propres relais et exigences de consommation.
    
4. **Interface utilisateur améliorée** : Bien que l’interface actuelle permette de contrôler les relais et de consulter les données, une interface graphique plus développée permettrait une gestion plus intuitive, avec la possibilité de visualiser en temps réel les graphiques de consommation et de contrôler les relais depuis une application mobile ou une interface web.
    
5. **Automatisation avancée** : En intégrant des règles plus complexes et des interactions avec d'autres appareils intelligents (comme des thermostats ou des panneaux solaires), le système pourrait automatiser encore plus finement la gestion énergétique en fonction des conditions extérieures et des besoins spécifiques.

