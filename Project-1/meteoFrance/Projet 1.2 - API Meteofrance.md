## Sommaire

1. **Introduction**
    - Contexte du projet
    - Objectifs et enjeux
2. **Authentification et récupération du token OAuth2**
    - Création d'un compte et abonnement à l'API
    - Obtention du token OAuth2
3. **Récupération des données météorologiques**
    - Analyse du code initial
    - Récupération de la liste des stations
    - Calcul de la station la plus proche
4. **Récupération des observations météorologiques**
    - Utilisation de l'API avec la station identifiée
    - Données reçues et analyse
5. **Limitations et perspectives**
    - Contraintes de l'API (données historiques uniquement)
    - Adaptabilité du projet pour d'autres usages
6. **Conclusion**
    - Résumé des résultats
    - Évolutions possibles

***
## 1. Introduction

### 1.1 Contexte du projet

Aujourd’hui, avoir accès à des données météo fiables est super utile dans plein de domaines : agriculture, transport, gestion d’énergie, etc. Pour ça, Météo France met à disposition une API qui permet de récupérer des infos en temps réel ou passées depuis différentes stations météorologiques en France. L’idée derrière ce projet était d’explorer cette API, voir comment elle fonctionne et utiliser ses données pour trouver la station la plus proche d’un point donné, puis afficher ses relevés météo.

Pour y arriver, plusieurs étapes ont été nécessaires. D’abord, il a fallu créer un compte et s’abonner à l’API pour récupérer un **token OAuth2**, qui est une sorte de clé permettant d’accéder aux données. Ensuite, en récupérant la liste des stations météo disponibles, on a pu utiliser leurs coordonnées GPS pour calculer laquelle était la plus proche grâce à une formule mathématique appelée **Haversine**. Une fois cette station trouvée (ici, celle de **Dorans**), on a pu envoyer une requête à l’API pour obtenir ses relevés météo, comme la température, l’humidité ou encore la pression atmosphérique.

### 1.2 Objectifs et enjeux

L’objectif de ce projet était avant tout de tester et comprendre le fonctionnement de l’API de Météo France. Ça permet de se familiariser avec des concepts comme l’**authentification OAuth2**, l’envoi de **requêtes API**, la gestion des réponses en **JSON**, et l’exploitation des données récupérées.

Un des points importants à prendre en compte est que l’API ne permet que d’accéder aux **données passées**, pas aux prévisions. Du coup, ça limite son utilisation dans certains projets, mais ça reste intéressant pour analyser des tendances météo. Autre contrainte : il y a des restrictions sur le nombre de requêtes qu’on peut faire en peu de temps, donc il faut faire attention à bien optimiser les appels à l’API pour éviter les blocages.

Enfin, ce projet a aussi été une bonne occasion de manipuler des **coordonnées GPS** et de travailler sur des calculs de distance, ce qui peut être super utile dans d’autres applications où on doit localiser des objets ou des points d’intérêt.

***
## 2. Authentification et récupération du token OAuth2

### 2.1 Création d’un compte et abonnement à l’API

Avant de pouvoir utiliser l’API de Météo France, il faut d’abord créer un compte sur leur portail développeur et s’abonner à l’API de données d’observation. Cet abonnement donne accès à un ensemble de services permettant de récupérer des relevés météo en temps réel ou passés.

L’abonnement en question permet d’effectuer jusqu’à **50 requêtes par minute**, ce qui est largement suffisant pour la plupart des usages courants. L’accès à l’API est valide jusqu’au **13 février 2027**, ce qui laisse une bonne marge pour tester et exploiter les données sans se soucier d’un renouvellement immédiat.

### 2.2 Obtention du token OAuth2

L’API de Météo France utilise un système d’**authentification OAuth2** pour sécuriser l’accès aux données. Pour pouvoir interagir avec l’API, il faut d’abord récupérer un **token OAuth2**, qui servira de clé d’accès temporaire. Ce token doit être inclus dans chaque requête pour prouver que l’accès est autorisé.

L’obtention du token se fait en envoyant une requête **POST** au serveur d’authentification de Météo France avec les informations d’identification fournies lors de l’inscription. Voici la commande **cURL** permettant de récupérer le token :
```
curl -k -X POST https://portail-api.meteofrance.fr/token \
-d "grant_type=client_credentials" \
-H "Authorization: Basic UGNaSkd4SU9fN3NQSHRNcHJjTENmWnM4M0dBYTp3R25PV1BmM1JkTHlNM2tyWGZQOTdGdFRjajBh"
```
Une fois cette requête envoyée, le serveur retourne un token sous forme de **chaîne de caractères** (JSON) qu’il faudra inclure dans l’en-tête de chaque requête API pour authentifier l’accès. Ce token a une durée de validité limitée et devra être renouvelé régulièrement pour continuer à utiliser l’API.

***

## 3. Récupération des données météorologiques

Ce script Python permet de récupérer des données météorologiques en plusieurs étapes :

1. **Authentification auprès de l’API de Météo France** via un token OAuth2.
2. **Téléchargement de la liste des stations météorologiques** depuis Météo France.
3. **Stockage local des données** sous forme de fichier JSON pour éviter des requêtes répétées.
4. **Calcul de la station météo la plus proche** d’un point donné en utilisant la formule de Haversine.

Nous allons analyser chaque étape en détail :

### 3.1 Authentification via OAuth2

Vous utilisez un système d'authentification OAuth2 pour obtenir un token d'accès à l'API de Météo France. Le token est nécessaire pour faire des requêtes sur l'API publique et accéder aux informations de stations météorologiques.

```python
url_token = "https://portail-api.meteofrance.fr/token"
data_token = {'grant_type': 'client_credentials'}
headers_token = {
    'Authorization': 'Basic ...',
    'Content-Type': 'application/x-www-form-urlencoded'
}
response_token = requests.post(url_token, data=data_token, headers=headers_token)
```

### 3.2 Téléchargement de la liste des stations météorologiques

Une fois le token obtenu, vous envoyez une requête GET pour récupérer la liste des stations météorologiques. Si la requête est réussie (code 200), vous traitez les données et les convertissez en JSON. Ce processus permet d'éviter les requêtes répétées en enregistrant les données localement dans un fichier `meteoFrance.json`.
```python
url = "https://public-api.meteofrance.fr/public/DPObs/v1/liste-stations"
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
response = requests.get(url, headers=headers)
```

### 3.3 Stockage des données dans un fichier JSON

Les données récupérées sous forme de CSV sont lues et converties en JSON pour un stockage local. Cela permet d'éviter de refaire la même requête à l'API à chaque fois, et ainsi économiser des ressources. Le fichier JSON est ensuite sauvegardé dans le même répertoire que le script.
```python
json_data = []
for row in csv_reader:
    station = {
        "id": row[0],
        "wmo": row[1] if row[1] else None,
        "name": row[2],
        "latitude": float(row[3]),
        "longitude": float(row[4]),
        "altitude": int(row[5]),
        "start_date": row[6],
        "type": row[7]
    }
    json_data.append(station)

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=4, ensure_ascii=False)
```

### 3.4 Calcul de la station la plus proche

La fonction `find_nearest_station` calcule la station la plus proche en utilisant la formule de Haversine, qui permet de déterminer la distance entre deux points géographiques (en l'occurrence, latitude et longitude). Elle prend en entrée les coordonnées d'un point donné et trouve la station la plus proche en utilisant la distance minimale calculée.
``` python
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def find_nearest_station(lat, lon):
    stations = load_meteo_data()
    nearest_station = min(stations, key=lambda station: haversine(lat, lon, station["latitude"], station["longitude"]))
    return nearest_station
```

### 3.5 Résultat

Pour les coordonnées spécifiées (latitude: 47.49520, longitude: 6.802791), la station météorologique la plus proche est :
```json
{
	'id': '90035001',
	'wmo': '07296', 
	'name': 'DORANS', 
	'latitude': 47.591667, 
	'longitude': 6.837, 
	'altitude': 401, 
	'start_date': '2008-11-05', 
	'type': 'RADOME'
}
```

## 4. Récupération des observations météorologiques

Cette section montre comment utiliser l'API de Météo France pour récupérer les observations météorologiques à une date et une heure spécifiées pour une station donnée.

### 4.1 URL de l'API pour récupérer les observations météorologiques

``` python
url = f"https://public-api.meteofrance.fr/public/DPObs/v1/station/horaire?id_station=90035001&date={date_formatted}&format=json"
```

Cette ligne définit l'URL de l'API de Météo France pour récupérer les observations météorologiques horaires à partir de la station `90035001`. Voici une explication détaillée des différents paramètres dans l'URL :

- `id_station=90035001` : C'est l'ID unique de la station météorologique pour laquelle nous souhaitons récupérer les données. Dans ce cas, il correspond à une station précise.
- `date={date_formatted}` : Cela permet de spécifier la date et l'heure de la requête. La variable `date_formatted` contient la date formatée sous le format `YYYY-MM-DDTHH:MM:SSZ` pour une heure précise.
- `format=json` : Cela spécifie que la réponse de l'API doit être en format JSON. C'est l'option la plus couramment utilisée pour récupérer les données dans un format structuré et facile à analyser.

### 4.2 Analyse des données reçues

Voici la réponse JSON que nous avons reçue de l'API :

```json
[
    {
        "lat": 47.591667,
        "lon": 6.837,
        "geo_id_insee": "90035001",
        "reference_time": "2025-02-20T07:10:08Z",
        "insert_time": "2025-02-20T07:04:36Z",
        "validity_time": "2025-02-20T07:00:00Z",
        "t": 276.35,
        "td": 275.95,
        "tx": 276.45,
        "tn": 276.15,
        "u": 97,
        "ux": 97,
        "un": 94,
        "dd": 330,
        "ff": 0.7,
        "dxy": 320,
        "fxy": 1.6,
        "dxi": 310,
        "fxi": 2.1,
        "rr1": 0,
        "t_10": 276.55,
        "t_20": 276.75,
        "t_50": 277.75,
        "t_100": 279.65,
        "vv": 2230,
        "etat_sol": 1,
        "sss": 0,
        "n": 8,
        "insolh": null,
        "ray_glo01": null,
        "pres": 97740,
        "pmer": 102680
    }
]
```

###### 4.2.1 lat et lon
- **lat** (Latitude) : La latitude de la station météorologique. Ici, la valeur `47.591667` correspond à un point géographique situé à environ 47.59° au nord de l'équateur.
- **lon** (Longitude) : La longitude de la station météorologique. La valeur `6.837` indique un emplacement à environ 6.84° à l'est du méridien de Greenwich.
###### 4.2.2 geo_id_insee
- **geo_id_insee** : Un identifiant unique pour la station météorologique basé sur le code INSEE, utilisé en France pour identifier les communes ou, dans ce cas, une station météorologique. L'ID `90035001` correspond à cette station particulière.
###### 4.2.3 reference_time
- **reference_time** : L'heure à laquelle les données ont été collectées, au format ISO 8601. Ici, `2025-02-20T07:10:08Z` signifie que les données ont été collectées le 20 février 2025 à 07h10 UTC (heure universelle).
###### 4.2.4 insert_time
- **insert_time** : L'heure à laquelle les données ont été insérées ou enregistrées dans la base de données. Ici, `2025-02-20T07:04:36Z` indique que l'enregistrement a eu lieu quelques minutes avant la collecte réelle des données.
###### 4.2.5 validity_time
- **validity_time** : L'heure de validité des données, soit la période à laquelle les informations sont censées être exactes. Ici, `2025-02-20T07:00:00Z` signifie que les données sont valides à partir du 20 février 2025, 07h00 UTC.
###### 4.2.6 t (Température)
- **t** : La température mesurée à la station météorologique, exprimée en Kelvin. Ici, `276.35` K correspond à environ 3.2°C (Kelvin -> Celsius : 276.35 - 273.15).
###### 4.2.7 td (Température du point de rosée)
- **td** : La température du point de rosée, c'est-à-dire la température à laquelle l'air devient saturé d'humidité et commence à condenser. La valeur `275.95` K est environ 2.8°C.
###### 4.2.8 tx (Température maximale)
- **tx** : La température maximale mesurée pendant la période de validité des données, ici `276.45` K (environ 3.3°C).
###### 4.2.9 tn (Température minimale)
- **tn** : La température minimale mesurée pendant la période de validité des données, ici `276.15` K (environ 3.0°C).
###### 4.2.10 u (Humidité relative)
- **u** : L'humidité relative de l'air en pourcentage, indiquant le niveau d'humidité par rapport à la quantité maximale que l'air peut contenir à une température donnée. Ici, `97%` signifie que l'air est presque saturé en humidité.
###### 4.2.11 ux et un
- **ux** : L'humidité relative maximale mesurée pendant la période de validité, ici `97%`.
- **un** : L'humidité relative minimale mesurée pendant la période de validité, ici `94%`.
###### 4.2.12 dd (Direction du vent)
- **dd** : La direction du vent, exprimée en degrés (0° = nord, 90° = est, 180° = sud, 270° = ouest). Ici, `330°` signifie que le vent vient du nord-ouest.
###### 4.2.13 ff (Vitesse du vent)
- **ff** : La vitesse du vent en mètres par seconde. Ici, `0.7` m/s signifie un vent modéré.
###### 4.2.14 dxy, fxy, dxi, fxi
- Ces valeurs sont liées à la mesure de la direction et de la vitesse du vent, en particulier pour les phénomènes de vent extrême ou pour des vents de grande vitesse :
    - **dxy** : Direction du vent sur 10 minutes.
    - **fxy** : Vitesse du vent sur 10 minutes.
    - **dxi** : Direction du vent sur 1 minute.
    - **fxi** : Vitesse du vent sur 1 minute.
###### 4.2.15 rr1
- **rr1** : La quantité de précipitations mesurée sur la dernière heure, en millimètres. Ici, la valeur `0` indique qu'il n'y a pas eu de précipitations mesurées.
###### 4.2.16 t_10, t_20, t_50, t_100
- **t_10**, **t_20**, **t_50**, **t_100** : Ces valeurs représentent les températures mesurées à différentes hauteurs (en mètres) dans l'atmosphère. Les chiffres correspondent à l'altitude à laquelle les températures ont été mesurées :
    - **t_10** : Température à 10 mètres d'altitude.
    - **t_20** : Température à 20 mètres d'altitude.
    - **t_50** : Température à 50 mètres d'altitude.
    - **t_100** : Température à 100 mètres d'altitude.
###### 4.2.17 vv
- **vv** : La visibilité, exprimée en mètres. La valeur `2230` indique que la visibilité à la station est de 2230 mètres.
###### 4.2.18 etat_sol
- **etat_sol** : L'état du sol à la station, où `1` signifie que le sol est sec. Cela peut aussi indiquer d'autres états comme mouillé, neigeux, etc.
###### 4.2.19 sss
- **sss** : Cela peut être un indicateur de la salinité de l'eau ou d'un autre phénomène lié à l'état des eaux près de la station. La valeur `0` signifie probablement que cet indicateur n'est pas mesuré ou n'est pas pertinent dans ce contexte.
###### 4.2.20 n
- **n** : Le nombre d'observations ou de relevés effectués pendant la période de validité. Ici, `8` pourrait signifier qu'il y a eu 8 relevés distincts.
###### 4.2.21 insolh
- **insolh** : L'ensoleillement horaire, probablement la quantité d'énergie solaire reçue par la station par heure. La valeur `null` signifie que cette donnée n'a pas été mesurée ou n'est pas disponible.
###### 4.2.22 ray_glo01
- **ray_glo01** : Cela pourrait faire référence à l'irradiance globale ou à la puissance solaire reçue. La valeur `null` indique qu'aucune donnée n'est disponible à ce sujet.
###### 4.2.23 pres
- **pres** : La pression atmosphérique mesurée à la station, en Pascals (Pa). Ici, la valeur `97740` Pa correspond à environ 977.4 hPa (hectopascals).
###### 4.2.24 pmer
- **pmer** : La pression atmosphérique corrigée ou mesurée au niveau de la mer, exprimée également en Pascals. La valeur `102680` Pa correspond à environ 1026.8 hPa.

## 5. Limitations et perspectives

### 5.1 Contraintes de l'API (données historiques uniquement)

L'une des principales limitations rencontrées dans ce projet réside dans les données disponibles via l'API de Météo France. En effet, cette API fournit uniquement des **données historiques** et non des **prévisions ou des mesures en temps réel**. Cela peut poser problème dans un projet de délestage du réseau électrique, car ces informations ne sont pas directement exploitables pour une gestion dynamique en temps réel des ressources énergétiques.

Les données de température, d'humidité, de vitesse du vent, etc., sont collectées à des moments précis, mais il est difficile d'agir de manière réactive à partir de ces informations lorsqu'on parle de **délestage en temps réel** pour optimiser la consommation ou anticiper les besoins en énergie. Le fait que les données soient disponibles avec un certain délai peut ne pas correspondre aux exigences de réactivité nécessaires pour un tel projet.

### 5.2 Adaptabilité du projet pour d'autres usages

Malgré cette contrainte, le projet peut être **adapté à d'autres usages** où l'important n'est pas la réactivité en temps réel. Voici quelques perspectives d'utilisation :

- **Applications en agriculture ou en gestion des ressources naturelles** : Les données historiques sur la température, l'humidité et le vent peuvent être utiles pour prédire des événements tels que des vagues de chaleur, la gestion de l'irrigation, ou encore les risques d'incendie, là où des prévisions sur le long terme sont plus importantes.
- **Optimisation de la gestion énergétique à long terme** : Si l'objectif est de prédire la consommation d'énergie sur une longue période, des données historiques peuvent être utilisées pour ajuster les modèles de consommation, en particulier dans le cas des énergies renouvelables (éolien, solaire), qui dépendent fortement des conditions météorologiques.

En résumé, bien que l'API de Météo France soit limitée pour ce projet de **délestage en temps réel**, elle pourrait être une ressource précieuse dans des contextes d'analyse climatologique ou d'optimisation énergétique à plus long terme, à condition d'adapter le projet en conséquence.

## 6. Conclusion

### 6.1 Résumé des résultats

Le projet a permis d'établir une connexion avec l'API de Météo France afin de récupérer des données météorologiques historiques à travers une série d'étapes bien définies. Nous avons réalisé une **authentification via OAuth2**, récupéré la **liste des stations météorologiques**, stocké les données localement pour éviter des requêtes répétées, et utilisé la **formule de Haversine** pour déterminer la station la plus proche d'un point donné.

Bien que les données récupérées soient détaillées (température, humidité, vitesse du vent, etc.), elles présentent certaines limitations, notamment en ce qui concerne leur caractère **historique et non en temps réel**. Ces informations, bien que pertinentes pour des analyses climatologiques ou énergétiques à moyen ou long terme, ne sont pas directement exploitables pour un **délestage dynamique en temps réel**, comme envisagé initialement dans le projet.

Les résultats du projet ont permis de démontrer que les données météorologiques peuvent être stockées et utilisées efficacement dans un cadre d'analyse climatologique, mais qu'une évolution vers des solutions en temps réel est nécessaire pour un usage plus pratique dans des projets énergétiques immédiats.

### 6.2 Évolutions possibles

Pour que ce projet atteigne son plein potentiel, plusieurs évolutions sont possibles :
**Utilisation d'algorithmes prédictifs** : En associant des données météorologiques en temps réel à des modèles prédictifs, il serait possible d’anticiper les périodes de forte demande en énergie, en particulier pendant les vagues de chaleur ou les périodes de grand froid. L'utilisation de **modèles d’apprentissage automatique** pourrait améliorer l'efficacité du système.
**Amélioration de la précision des prévisions météorologiques** : L'intégration de modèles de prévision météorologique avancés pour ajuster les informations en fonction des tendances et des événements climatiques (tempêtes, vagues de chaleur) pourrait offrir des informations plus fiables et pertinentes pour des décisions en temps réel.

En résumé, ce projet a jeté les bases d'une gestion énergétique utilisant les données météorologiques, mais il serait nécessaire d'évoluer vers des solutions en temps réel pour qu'il devienne réellement utile dans un contexte de gestion dynamique du réseau électrique.