import requests
url = "http://api"
data = {
    'Authorization': 'Basic y59Pr098w7YimT1oTgSDidALlB2YmBha==',
    'Content-Type': 'application/x-www-form-urlencoded',
}
response = requests.post(url, headers=data)
status_code = response.status_code
print('status code = ', status_code)
infos_rte_token = response.json()
print('infos RTE token = ', infos_rte_token)
token = infos_rte_token['access_token']
print('token = ',token)
