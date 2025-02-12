import json
import os

# Charger les données JSON
file = "\\ecowatt.json"
script_dir = os.path.dirname(os.path.abspath(__file__))

with open( script_dir+file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Liste chaînée pour stocker les résultats
class Node:
    def __init__(self, jour, pas):
        self.jour = jour
        self.pas = pas
        self.next = None

# Fonction pour ajouter un élément à la liste chaînée
def add_to_linked_list(head, jour, pas):
    new_node = Node(jour, pas)
    if not head:
        return new_node
    last = head
    while last.next:
        last = last.next
    last.next = new_node
    return head

# Extraire les heures et les jours où hvalue est 0
head = None
for signal in data['signals']:
    jour = signal['jour']
    for entry in signal['values']:
        if entry['hvalue'] == 0:
            head = add_to_linked_list(head, jour, entry['pas'])

# Afficher la liste chaînée
current = head
while current:
    print(f"Jour: {current.jour}, Heure: {current.pas}h")
    current = current.next