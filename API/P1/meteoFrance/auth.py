import requests
import json
import time

url = "https://public-api.meteofrance.fr/public/DPObs/v1"
data = {
    'Authorization': 'Basic eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4N2ZkNmViZC1hNzc0LTRhMjctOTc1Ny0wMzgzNDhjMWU3NzAiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IlBjWkpHeElPXzdzUEh0TXByY0xDZlpzODNHQWEiLCJuYmYiOjE3Mzk0MzY5MDIsImF6cCI6IlBjWkpHeElPXzdzUEh0TXByY0xDZlpzODNHQWEiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3Mzk0NDA1MDIsImlhdCI6MTczOTQzNjkwMiwianRpIjoiYjY5YjQzZTgtMmExMS00YTlmLTk2MjUtZWQ0MWI5MDZiYTJmIiwiY2xpZW50X2lkIjoiUGNaSkd4SU9fN3NQSHRNcHJjTENmWnM4M0dBYSJ9.cyTAU-FV3wteMLNOC48YR_v-ZztItWxTAtPUX0rB-nt9WikU5rqp9LnhdSPVSqChdWsPH_z2fk6khrGP8vRkniOK5_nhmUxnGtlzBEPWFFIaK_0595Hw1pDpgQtkocDW-d-gUVKmIHQqq1gUARR0YY6V_9eJ_Wq0G-HuKZ_Tsix6pvZr7A1604lmOWMBw88TB6iBZI_EmgSqH7sgfM3ZedHSmzdpJNTV_uzDpkFVG0XrwhtpeYZ8Sq3Hr-KexoUTx4IE99GfZep00jht5s6wxuea-JoJaNjMbHkr0NDEfqmdenZx9wYn9PBNaIzYoo8aLPc-iMGuP6jjL9kXS52QDg',
    'Content-Type': 'application/x-www-form-urlencoded',
}
response = requests.post(url, headers=data)
status_code = response.status_code
print('status code = ', status_code)
infos_rte_token = response.json()
print('infos RTE token = ', infos_rte_token)
token = infos_rte_token['access_token']
print('token = ',token)

# Fichier où enregistrer les données
file = "ecowatt.json"

# Token d'accès (remplace par un token valide si nécessaire)
token = "466Cww165KVW6f1nohjMQwqmQWnUd2C7AXTOHQjcxRp7AcoRW9CMWX"

# URL de l'API Ecowatt
url = "https://digital.iservices.rte-france.com/open_api/ecowatt/v5/signals"

# Headers corrigés
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",  # Corrige le Content-Type pour demander du JSON
}

# Tentative avec gestion du 429 Too Many Requests
max_retries = 5
retry_delay = 10  # Attendre 10 secondes en cas de 429
for attempt in range(max_retries):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            infos_rte_data_ecowatt_json = response.json()
            print("Données reçues :", infos_rte_data_ecowatt_json)
            
            # Sauvegarde en fichier JSON
            with open(file, "w") as f:
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
