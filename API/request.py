import requests

response = requests.get("http://localhost:5000/increment")
print(response.json())  # Affichera {"count": X}
