# Arbok 🚀

**Arbok** est un projet IoT qui intègre plusieurs API et modules afin de gérer des équipements électriques et surveiller la consommation d'énergie 🌍. Ce projet utilise des technologies comme **OAuth2** 🔐 pour sécuriser les échanges, l'**API Ecowatt** de RTE ⚡, et des relais **Phidget** pour contrôler des appareils à forte consommation d'énergie. Le projet est structuré en plusieurs parties pour permettre une gestion efficace de l'énergie et un contrôle sécurisé des équipements.

## Arborescence du projet 📂

```
ARBOK
│   LICENSE
│   Pass.md
│   README.md
│
├───Project-1
│   ├───ecoWatt
│   │   │   Projet 1.1 - API Ecowatt.md
│   │   │
│   │   ├───Request-V0.1
│   │   │       auth.py
│   │   │       ecowatt.json
│   │   │       ecowatt_api_request.py
│   │   │       jsonreader.py
│   │   │
│   │   └───Request-V2.0
│   │           ecowatt.json
│   │           Request-Ecowatt-API.py
│   │
│   └───meteoFrance
│           curl
│           Données_d’observation_swagger.json
│           meteoFrance.json
│           Projet 1.2 - API Meteofrance.md
│           Request-Ecowatt-API-Data.py
│           Request-Ecowatt-API-Station.py
│
├───Project-2
│   │   Projet 3 - delestage.md
│   │
│   ├───Delestage
│   │       delestage_pilotage_phidget.py
│   │       delestage_pilotage_phidget_v2.py
│   │
│   ├───Serveur
│   │       API-Delestage-v1.0.py
│   │       API-Delestage-v2_0.py
│   │       API-DelestageV-0.1.py
│   │       mode.json
│   │
│   ├───WEB
│   │       delestage.css
│   │       delestage.html
│   │       script.js
│   │
│   └───__pycache__
│           API-Delestage-v2_0.cpython-311.pyc
│
└───Project-3
    │   Projet 3 - API ESP et RASP.md
    │
    ├───API-RASP
    │       BasicAPI-v0.1.py
    │       BasicAPI-v2.0.py
    │       counter.txt
    │
    ├───ESP
    │   ├───API
    │   │   ├───BasicAPI-v0.1
    │   │   │       BasicAPI-v0.1.ino
    │   │   │
    │   │   ├───BasicAPI-v1.0
    │   │   │       BasicAPI-v1.0.ino
    │   │   │
    │   │   ├───BasicAPI-v1.1
    │   │   │       BasicAPI-v1.1.ino
    │   │   │
    │   │   ├───TempAPI-v1.0
    │   │   └───TempAPI-v2.1
    │   │           TempAPI-v2.1.ino
    │   │
    │   └───Temperature
    │       ├───Temp-v0.1
    │       │       Temp-v0.1.ino
    │       │
    │       ├───Temp-v1.0
    │       │       Temp-v1.0.ino
    │       │
    │       └───Temp-v2.0
    │               Temp-v2.0.ino
    │
    ├───Request
    │       request-v0.1.py
    │       request-v2.0.py
    │       TokenAccess.py
    │
    ├───WEB
    │       API.html
    │       style.css
    │
    └───__pycache__
            requests.cpython-311.pyc
```

#### `LICENSE`
- **Description :** Ce fichier contient la licence sous laquelle le projet est distribué, en l'occurrence la licence **MIT**. Il définit les droits d'utilisation, de modification et de distribution du code source.
#### `Pass.md`
- **Description :** Ce fichier peut contenir des informations sensibles sur les mots de passe, les tokens ou les clés API utilisées dans le projet. Il est important de ne pas partager ce fichier publiquement.
#### `README.md`
- **Description :** Ce fichier contient la documentation du projet **Arbok**, expliquant le but du projet, les fonctionnalités principales, l'arborescence, l'installation, et les étapes de configuration. Il sert de guide pour les développeurs ou utilisateurs qui souhaitent comprendre ou utiliser le projet.
### **Project-1 : API Ecowatt et Météo France**
#### `ecoWatt`
- **Description :** Ce répertoire contient des scripts permettant d’interagir avec l'API **Ecowatt** de RTE pour surveiller l’état de la consommation énergétique en France.
- **`Request-V0.1/` :**
    - `auth.py` : Script pour l'authentification avec l'API Ecowatt.
    - `ecowatt.json` : Fichier de stockage des données extraites de l'API Ecowatt.
    - `ecowatt_api_request.py` : Script qui effectue une requête vers l'API pour obtenir des données.
    - `jsonreader.py` : Script pour lire et traiter les données dans `ecowatt.json`.
- **`Request-V2.0/` :**
    - `ecowatt.json` : Nouveau format de stockage des données Ecowatt.
    - `Request-Ecowatt-API.py` : Nouvelle version du script pour récupérer les données de l’API Ecowatt.
#### `meteoFrance`
- **Description :** Ce répertoire contient des scripts pour récupérer des données météorologiques via l'API de Météo France.
- **`curl/` :** Utilisation de `curl` pour interagir avec l'API Météo France.
- **`Données_d’observation_swagger.json` :** Fichier JSON généré par l'API qui décrit les observations météorologiques.
- **`meteoFrance.json` :** Données météorologiques récupérées et stockées.
- **`Projet 1.2 - API Meteofrance.md` :** Documentation expliquant l'usage de l'API Météo France et son intégration dans le projet.
- **`Request-Ecowatt-API-Data.py` :** Script pour effectuer une requête vers l'API et récupérer les données météorologiques.
- **`Request-Ecowatt-API-Station.py` :** Script pour récupérer les données par station météo.
---

### **Project-2 : Délestage**
#### `Delestage`
- **Description :** Ce répertoire contient les scripts pour gérer le **délestage énergétique** en utilisant les relais **Phidget**.
- **`delestage_pilotage_phidget.py` :** Script principal pour le pilotage des relais **Phidget** afin de couper les systèmes de consommation d'énergie.
- **`delestage_pilotage_phidget_v2.py` :** Version mise à jour du script pour une meilleure gestion du délestage.
#### `Serveur`
- **Description :** Ce répertoire contient les fichiers du serveur qui gère les requêtes API pour le délestage.
- **`API-Delestage-v1.0.py` :** Première version de l'API qui expose les endpoints pour contrôler les relais.
- **`API-Delestage-v2_0.py` :** Version 2 de l'API avec des améliorations.
- **`API-DelestageV-0.1.py` :** Ancienne version du serveur API pour gérer les relais.
- **`mode.json` :** Fichier de configuration qui peut contenir les paramètres de mode du système de délestage.
#### `WEB`
- **Description :** Ce répertoire contient les fichiers frontend pour l'interface utilisateur du délestage.
- **`delestage.css` :** Styles CSS pour la page Web du délestage.
- **`delestage.html` :** Page HTML qui permet de visualiser et de contrôler l'état du délestage.
- **`script.js` :** Script JavaScript pour gérer les interactions avec l'interface web.
---
### **Project-3 : API ESP et Rasp**
#### `API-RASP`
- **Description :** Ce répertoire contient des scripts API pour interagir avec les appareils **Raspberry Pi**.
- **`BasicAPI-v0.1.py` :** Première version d'une API simple pour interagir avec le Raspberry Pi.
- **`BasicAPI-v2.0.py` :** Nouvelle version de l'API avec des améliorations.
- **`counter.txt` :** Fichier de stockage pour des données simples, comme un compteur.
    
#### `ESP`
- **Description :** Ce répertoire contient les scripts pour les appareils **ESP32** et **ESP8266**.
- **`API/` :** Ce répertoire contient différents scripts pour gérer des API sur les microcontrôleurs ESP.
    - **`BasicAPI-v0.1/`** : Code pour une API basique.
    - **`BasicAPI-v1.0/`** : Version améliorée de l’API.
    - **`BasicAPI-v1.1/`** : Dernière version stable de l’API.
    - **`TempAPI-v1.0/` :** API pour gérer les données de température.
    - **`TempAPI-v2.1/` :** Version mise à jour pour gérer les températures.
- **`Temperature/` :** Répertoire contenant des scripts pour lire et traiter les données de température.
    - **`Temp-v0.1/` :** Première version du script pour récupérer la température.
    - **`Temp-v1.0/` :** Version mise à jour avec des améliorations.
    - **`Temp-v2.0/` :** Dernière version stable du script.

#### `Request`
- **Description :** Ce répertoire contient des scripts pour effectuer des requêtes HTTP et gérer les tokens OAuth2 pour la sécurité.
- **`request-v0.1.py` :** Première version du script pour effectuer des requêtes.
- **`request-v2.0.py` :** Version améliorée du script pour gérer des appels API plus complexes.
- **`TokenAccess.py` :** Script pour gérer l’accès sécurisé aux API via OAuth2.
    
#### `WEB`
- **Description :** Répertoire contenant les fichiers frontend pour l’API ESP.
- **`API.html` :** Interface Web pour interagir avec les API du projet **ESP**.
- **`style.css` :** Styles CSS pour la page API.

## Description des fonctionnalités ⚙️

### 1. **API Ecowatt** (RTE)
L'API **Ecowatt** permet de connaître les pics d'utilisation du réseau électrique français ⚡. L'API effectue des requêtes sécurisées à l'API Ecowatt pour obtenir ces données, puis les stocke sous forme de fichier JSON (`ecowatt.json`).

### 2. **Délestage avec Phidget** 💡
Le projet utilise le module **Phidget Interface Kit 0/0/8** pour contrôler des relais. Ces relais sont connectés à des LED représentant des systèmes consommateurs d'énergie. L'objectif est d'éteindre ces systèmes lorsque le réseau atteint des seuils de consommation critiques.

### 3. **Sécurisation avec OAuth2** 🔐
Les échanges avec les API sont sécurisés via **OAuth2**. Le serveur de base (dans `P3`) permet d'effectuer des requêtes authentifiées pour récupérer des informations depuis l'API **Ecowatt**, et pour gérer l'état des relais **Phidget** via des requêtes authentifiées.

### 4. **Interface Web** 🌐
Le projet inclut une interface web permettant de :
- Effectuer des requêtes API vers un **Raspberry Pi** ou un **ESP**.
- Contrôler l'état des relais **Phidget** à travers des interfaces de **délestage**.

## Installation 🛠️

1. **Clonez** ce dépôt sur votre machine locale :
   ```
   git clone https://github.com/ton-utilisateur/Arbok.git
   cd Arbok
   ```

2. Installez les **dépendances Python** nécessaires :
   ```
   pip install -r requirements.txt
   ```

3. Chargez le code sur les microcontrôleurs (**ESP32**, **Raspberry Pi**) à l'aide de l'IDE Arduino ou d'un autre outil adapté.

4. Suivez les instructions dans `Oauth2onRaspberry.md` pour configurer **OAuth2** sur le **Raspberry Pi**.

## 📦 Contributeurs

Ce projet a été réalisé par :

- **Guillaume Greder**  
- **Théo Marchand**  
- **Xavier Knoeppfler**  

## Contribution 🤝

Les contributions sont les bienvenues ! Pour suggérer des améliorations ou signaler des problèmes, ouvrez une **issue** ou soumettez une **pull request**.

## Licence 📜

Ce projet est sous licence **MIT**. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.
