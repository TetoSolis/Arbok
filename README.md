# Arbok 🚀

**Arbok** est un projet IoT qui intègre plusieurs API et modules afin de gérer des équipements électriques et surveiller la consommation d'énergie 🌍. Ce projet utilise des technologies comme **OAuth2** 🔐 pour sécuriser les échanges, l'**API Ecowatt** de RTE ⚡, et des relais **Phidget** pour contrôler des appareils à forte consommation d'énergie. Le projet est structuré en plusieurs parties pour permettre une gestion efficace de l'énergie et un contrôle sécurisé des équipements.

## Arborescence du projet 📂

nnn
Arbok/
├── API
│   ├── P1
│   │   ├── auth.py                 # Récupère le token OAuth2
│   │   ├── ecowatt_api_request.py   # Effectue une requête à l'API Ecowatt et l'enregistre dans ecowatt.json
│   │   ├── ecowatt.json             # Données récupérées de l'API Ecowatt
│   │   └── jsonreader.py            # Traite les données récupérées de l'API Ecowatt
│   ├── P2
│   │   ├── API-DelestageV-0.1.py    # Permet d'éteindre et allumer un relais Phidget via un site web
│   │   ├── delestage_pilotage_phidget.py  # Permet de contrôler un relais Phidget
│   │   └── delestage_pilotage_phidget_v2.py # Permet de contrôler un relais Phidget via les touches du clavier
│   └── P3
│       ├── BasicAPI-v0.1.py        # Serveur permettant des requêtes simples
│       ├── BasicAPI-v2.0.py        # Serveur permettant des requêtes authentifiées
│       ├── counter.txt             # Compte le nombre de requêtes
│       ├── Oauth2onRaspberry.md    # Guide pour implémenter OAuth2 sur un Raspberry Pi
│       ├── __pycache__
│       │   └── requests.cpython-311.pyc
│       ├── request-v0.1.py         # Permet des requêtes sans authentification
│       ├── request-v2.0.py         # Permet des requêtes avec authentification
│       └── TokenAccess.py          # Permet de récupérer un token OAuth2
├── ESP
│   ├── BasicAPI-v0.1              # Serveur de requêtes simple pour ESP
│   │   └── BasicAPI-v0.1.ino
│   ├── BasicAPI-v1.0              # Serveur de requêtes simple pour ESP
│   │   └── BasicAPI-v1.0.ino
│   ├── BasicAPI-v1.1              # Serveur de requêtes simple pour ESP
│   │   └── BasicAPI-v1.1.ino
│   ├── TempAPI-v2.1               # Serveur de requêtes avec authentification et capteur de température
│   │   └── TempAPI-v2.1.ino
│   ├── Temp-v0.1                  # Capteur de température
│   │   └── Temp-v0.1.ino
│   ├── Temp-v1.0                  # Capteur de température
│   │   └── Temp-v1.0.ino
│   └── Temp-v2.0                  # Capteur de température
│       └── Temp-v2.0.ino
├── Pass.md                        # Fichier contenant des informations de connexion sécurisées
├── README.md                      # Ce fichier
└── WEB
    ├── API.html                  # Interface web pour effectuer des requêtes API vers Raspberry Pi et ESP
    ├── delestage.html             # Interface pour contrôler le délestage des équipements
    └── style.css                  # Fichier CSS pour le style des pages web
nnn

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
   nnn
   git clone https://github.com/ton-utilisateur/Arbok.git
   cd Arbok
   nnn

2. Installez les **dépendances Python** nécessaires :
   nnn
   pip install -r requirements.txt
   nnn

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
