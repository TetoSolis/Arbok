import requests
url = "https://digital.iservices.rte-france.com/token/oauth"
data = {
    'Authorization': 'Basic OTRlMDkyZjctMjYyYS00NTIwLWFmYTctNDcwNGJlYjAwNjEyOjVmNjYyMTY1LWQ2MDctNGI3Ny1hNjYzLTc0Y2U0NzRlMDc1ZA==',
    'Content-Type': 'application/x-www-form-urlencoded',
}
response = requests.post(url, headers=data)
status_code = response.status_code
print('status code = ', status_code)
infos_rte_token = response.json()
print('infos RTE token = ', infos_rte_token)
token = infos_rte_token['access_token']
print('token = ',token)
