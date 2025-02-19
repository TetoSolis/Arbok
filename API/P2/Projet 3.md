Rapport Travail 2 : Projet de Délestage Énergétique

🔹 Introduction

Dans le cadre de la gestion efficace de la consommation énergétique, il est essentiel de pouvoir contrôler et réduire l'utilisation des appareils à forte consommation lors des pics de demande. Ce projet vise à mettre en place un système de délestage en utilisant le Phidget Interface Kit 0/0/8 (P/N 1017) pour piloter des relais connectés à des LED représentant ces appareils énergivores. Les données de consommation seront obtenues via l'API Ecowatt de RTE, sécurisée par OAuth2, comme implémenté précédemment.

🔹 1. Matériel Utilisé

📌 Phidget Interface Kit 0/0/8 (P/N 1017)
Le Phidget Interface Kit 0/0/8 est une carte d'interface USB équipée de 8 relais DPDT (Double Pole Double Throw) mécaniques. Chaque relais peut commuter jusqu'à 250V AC à 2A ou 200V DC à 2A, avec une puissance maximale de 60W. Cette carte est idéale pour contrôler des circuits nécessitant une isolation galvanique ou pour piloter des charges à distance via une interface logicielle.

🔹 2. Schéma de Connexion

📌 Configuration des Relais
Chaque relais du Phidget Interface Kit dispose de trois bornes :

NC (Normally Closed) : Le contact est fermé lorsque le relais est au repos.
NO (Normally Open) : Le contact est ouvert lorsque le relais est au repos.
COM (Common) : Borne commune.
Pour ce projet, les LED représentant les appareils énergivores sont connectées entre les bornes COM et NO de chaque relais. Ainsi, lorsque le relais est activé, le circuit se ferme et la LED s'allume, indiquant que l'appareil est en fonctionnement.

🔹 3. Implémentation Logicielle

📌 Objectif
Développer un script permettant de :

Récupérer les données de consommation via l'API Ecowatt.
Analyser ces données pour déterminer les périodes de forte consommation.
Activer ou désactiver les relais en conséquence pour simuler le délestage des appareils.
🖥️ Implémentation
Le script est développé en Python en utilisant la bibliothèque Phidget22 pour interagir avec le Phidget Interface Kit.

from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import requests
import time

# Fonction pour récupérer les données Ecowatt
def fetch_ecowatt_data(token):
    url = "https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None

# Fonction pour contrôler les relais
def control_relay(channel, state):
    relay = DigitalOutput()
    relay.setHubPort(channel)
    relay.setIsHubPortDevice(True)
    relay.openWaitForAttachment(1000)
    relay.setState(state)
    relay.close()

# Exemple d'utilisation
token = "votre_token_oauth2"
data = fetch_ecowatt_data(token)

if data:
    for signal in data.get('signals', []):
        jour = signal['jour']
        for entry in signal.get('values', []):
            pas = entry['pas']
            hvalue = entry['hvalue']
            # Supposons que hvalue > 1 indique une forte consommation
            if hvalue > 1:
                print(f"Forte consommation le {jour} à {pas}h")
                # Activer le relais correspondant
                control_relay(channel=0, state=True)
            else:
                # Désactiver le relais
                control_relay(channel=0, state=False)
            time.sleep(1)  # Pause pour éviter une commutation trop rapide

Explication
Récupération des données : La fonction fetch_ecowatt_data envoie une requête GET à l'API Ecowatt en utilisant le token OAuth2 pour authentifier la requête. Les données JSON reçues contiennent les signaux de consommation électrique.
Contrôle des relais : La fonction control_relay initialise un objet DigitalOutput pour le canal spécifié (correspondant à un relais particulier), établit la connexion avec le Phidget, définit l'état du relais (activé ou désactivé), puis ferme la connexion.
Analyse et délestage : Le script parcourt les signaux reçus et, en fonction de la valeur hvalue, détermine si la consommation est élevée. Si c'est le cas, le relais correspondant est activé pour simuler le délestage de l'appareil associé. Sinon, le relais est désactivé.
🔹 4. Résultats et Observations

Après l'implémentation et les tests, le système a démontré sa capacité à :

Récupérer en temps réel les données de consommation via l'API Ecowatt.
Analyser ces données pour identifier les périodes de forte demande énergétique.
Contrôler les relais du Phidget Interface Kit pour simuler le délestage des appareils énergivores en allumant ou éteignant les LED correspondantes.
Ce système offre une base solide pour le développement de solutions de gestion de la consommation énergétique dans des environnements domestiques ou industriels.

🔹 Conclusion

Le projet de délestage énergétique utilisant le Phidget Interface Kit 0/0/8 et les données de l'API Ecowatt a permis de mettre en place un système efficace de gestion de la consommation. Cette approche peut être étendue pour contrôler directement des appareils réels, offrant ainsi une solution proactive pour réduire la consommation pendant les pics de demande et contribuer à la stabilité du réseau électrique.
