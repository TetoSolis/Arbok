import requests
import json
import time
import os

# Fichier où enregistrer les données
file = "\\meteoFrance.json"
script_dir = os.path.dirname(os.path.abspath(__file__))

# Token d'accès (remplace par un token valide si nécessaire)
token = "eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ"

# URL de l'API Ecowatt
url = "https://public-api.meteofrance.fr:8280/public/DPObs/v1/liste-stations"

# Headers corrigés
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "*/*",  # Corrige le Content-Type pour demander du JSON
}

# Tentative avec gestion du 429 Too Many Requests
max_retries = 1
retry_delay = 10  # Attendre 10 secondes en cas de 429
for attempt in range(max_retries):
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        try:
            infos_rte_data_ecowatt_json = response.json()
            print("Données reçues :", infos_rte_data_ecowatt_json)
            
            # Sauvegarde en fichier JSON
            with open(script_dir+file, "w") as f:
                json.dump(infos_rte_data_ecowatt_json, f, indent=4)
            print(f"Données sauvegardées dans {file}")
            break
        
        except requests.exceptions.JSONDecodeError:
            print("Erreur: La réponse de l'API n'est pas un JSON valide.")
            print("Réponse brute:", response.text)
            break  # Sortir de la boucle car ce n'est pas un problème de rate limit

    elif response.status_code == 429:
        print(f"Erreur 429: Trop de requêtes. Tentative {attempt + 1}/{max_retries}. Réessai dans {retry_delay} sec...")
        time.sleep(retry_delay)
    
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        break
    
    
curl -X 'GET' 'http://public-api.meteofrance.fr:8280/public/DPObs/v1/liste-stations' 'accept: */*' -H 'Authorization: Bearer eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4N2ZkNmViZC1hNzc0LTRhMjctOTc1Ny0wMzgzNDhjMWU3NzAiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IlBjWkpHeElPXzdzUEh0TXByY0xDZlpzODNHQWEiLCJuYmYiOjE3Mzk0Mzc4MTcsImF6cCI6IlBjWkpHeElPXzdzUEh0TXByY0xDZlpzODNHQWEiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3Mzk0NDE0MTcsImlhdCI6MTczOTQzNzgxNywianRpIjoiZTQyMzc2ZTctNDkwNy00YTYzLWJhNGItNjVmNmJhYWIyYmFmIiwiY2xpZW50X2lkIjoiUGNaSkd4SU9fN3NQSHRNcHJjTENmWnM4M0dBYSJ9.Unl6DPDS8pBZol0CUr3TmiMrXUJ0GGUNRMEG6YVjrRCp6koMdcBnM2_-L97XYBeCN-JBuUBaeIf6lwp2xsxqXofcBtL0X64S61iY42w6fJOKV8oT6O2W2wdTRaVmyWx0KignuT-foeGC2y6ex0izGSPrOmCulgZ8CEmJn7tbrMClpOvRjoM0khTsn1ssRZaSIjlp7jM1bGOrl72lVvEqvZ-O-r4lMAy1gfJelRBVXp23AaqertCU3J2cID727u04cNGHiBvrZfnj43kRHvFt5-9156w0BwrOXvNSLiv3fWyoWhor8PZqBZdJx5A8l3JM-OMrH-DLfs3_XKgb3H1FvQ'