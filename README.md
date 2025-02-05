# Arbok

## Description

Arbok est un projet IoT ayant pour objectif de mettre en place un réseau sécurisé d'objets connectés répondant à un cahier des charges précis. Il s'inscrit dans le cadre de la SAÉ 6.IOM.01 du BUT Réseaux et Télécommunications, parcours Internet des Objets et Mobilités (IoM). Ce projet implique plusieurs technologies, notamment OAuth2, LoRa, MQTT et la connectivité par satellite avec Kinéis.

## Objectifs

1. **Sécurisation d'un objet connecté**
    
    - Implémentation d'OAuth2 sur un Raspberry Pi et un ESP32
        
    - Sécurisation des échanges avec l'API Ecowatt et l'API Météo France
        
    - Utilisation du module Phidget Interface Kit 0/0/8 P/N 1017 pour piloter des relais
        
2. **Interrogation d'un onduleur virtuel**
    
    - Expérimentation et mise en place d'une solution de gestion de l'énergie
        
3. **Interconnexion de deux maisons via une passerelle LoRa**
    
    - Utilisation des bornes MikroTik et du réseau The Things Network (TTN)
        
4. **Passerelle satellite avec carte Kinéis**
    
    - Mesure de température et niveau d'une retenue d'eau
        
    - Connexion de deux maisons séparées par une montagne
        
    - Implémentation d'une redondance des communications (LoRa / Kinéis) en mode normal et dégradé
        
    - Comparaison des performances (délai de réception...)
        
    - Ajout d'une seconde borne MikroTik pour redondance et enregistrement des données sur TTN
        
5. **Plateforme Octeus et IoT-Lab (expérimentation)**
    
    - Étude de l'interopérabilité avec des infrastructures existantes
        

## Technologies utilisées

- **ESP32 / ESP8266 / Raspberry Pi**
    
- **OAuth2** pour l'authentification et la sécurisation des accès
    
- **APIs Ecowatt et Météo France**
    
- **LoRa / The Things Network** pour la communication longue portée
    
- **Kinéis (IoT par satellite)**
    
- **MQTT** pour l'échange de données
    
- **Phidget Interface Kit** pour le pilotage d'actionneurs
    

## Installation et Configuration

### Prérequis

- Un ESP32, ESP8266 ou Raspberry Pi
    
- Une connexion Internet
    
- Accès aux APIs (Ecowatt, Météo France, Kinéis)
    
- Un module LoRa compatible TTN
    
- Un compte TTN et MikroTik configuré
    

### Étapes d'installation

6. Cloner le dépôt GitHub :
    
    ```
    git clone https://github.com/votre-repo/arbok.git
    cd arbok
    ```
    
7. Installer les dépendances requises (Python, Node.js, etc.).
    
8. Configurer les fichiers d'authentification OAuth2.
    
9. Déployer les scripts sur les équipements IoT.
    

## Structure du projet

```
/arbok
│── /firmware          # Code pour ESP32/ESP8266
│── /server            # Backend (authentification, API sécurisées)
│── /gateway           # Configuration LoRa et Kinéis
│── /docs              # Documentation et ressources
│── README.md          # Documentation principale
```

## Contributions

Les contributions sont les bienvenues ! Veuillez suivre les étapes suivantes :

10. Forker le projet
    
11. Créer une branche (`feature-ma-fonctionnalité`)
    
12. Soumettre une pull request
    

## Licence

Ce projet est sous licence MIT.

## Auteurs

- Teto et l'équipe du projet Arbok
